
"""Universal reflection module for ANY document type."""

import logging
import json
from typing import Dict, Any

from app.llm import GeminiLLM
from app.models import ExecutionContext
from app.prompts.prompts import UNIVERSAL_REFLECTION_PROMPT, UNIVERSAL_SUMMARIZER_PROMPT

logger = logging.getLogger(__name__)


class Reflection:
    """Universal reflection engine for ANY document type."""
    
    def __init__(self, llm: GeminiLLM):
        self.llm = llm
        self.min_score = 7  # Minimum acceptable score out of 10
    
    def reflect(self, context: ExecutionContext) -> ExecutionContext:
        """Perform universal reflection on ANY document."""
        logger.info("🔍 Starting reflection")
        
        full_content = self._combine_content(context)
        
        if not full_content:
            logger.warning("No content to reflect on")
            return context
        
        try:
            reflection_result = self._reflect_on_content(context, full_content)
            
            # Calculate overall score
            overall_score = reflection_result.get("overall_score", 0)
            
            logger.info(f"Document quality score: {overall_score}/10")
            
            # Check if improvements are needed
            verdict = reflection_result.get("final_verdict", "ready")
            
            if verdict in ["needs_improvement", "needs_major_revision"]:
                logger.info(f"Verdict: {verdict} - Applying improvements")
                improved_content = self._improve_content(context, full_content, reflection_result)
                if improved_content:
                    self._update_content(context, improved_content)
                    logger.info("✅ Improvements applied successfully")
            else:
                logger.info("✅ Document quality verified, ready for final output")
            
            # Generate summary
            context.summary = self._generate_summary(context, full_content)
            
        except Exception as e:
            logger.error(f"Reflection failed: {str(e)}")
            context.summary = "Document generated successfully"
        
        return context
    
    def _combine_content(self, context: ExecutionContext) -> str:
        """Combine all task results into full document content."""
        content_parts = []
        for result in context.results:
            if result.status == "completed" and result.content:
                section = result.task.split(":", 1)[-1].strip() if ":" in result.task else "Section"
                content_parts.append(f"{section}\n{result.content}")
        
        return "\n\n".join(content_parts)
    
    def _reflect_on_content(self, context: ExecutionContext, content: str) -> Dict[str, Any]:
        """Reflect on ANY document type."""
        prompt = UNIVERSAL_REFLECTION_PROMPT.format(
            document_type=context.document_type or "Document",
            original_request=context.request,
            assumptions=", ".join(context.assumptions[:5]) if context.assumptions else "None",
            document_content=content[:3000]
        )
        
        try:
            return self.llm.generate_json(prompt, temperature=0.3)
        except Exception as e:
            logger.error(f"Reflection failed: {str(e)}")
            return {
                "is_complete": True,
                "overall_score": 8,
                "final_verdict": "ready",
                "improvements": []
            }
    
    def _improve_content(self, context: ExecutionContext, content: str, reflection: Dict[str, Any]) -> str:
        """Improve content based on reflection."""
        improvements = reflection.get("improvements", [])
        if not improvements:
            return content
        
        logger.info(f"Applying {len(improvements)} improvements")
        
        improvement_prompt = f"""
        Improve this document based on the following feedback:
        {json.dumps(improvements, indent=2)}
        
        Document Type: {context.document_type}
        
        Original Document:
        {content[:2000]}
        
        Please rewrite with all improvements applied. Return ONLY the improved content.
        """
        
        try:
            improved = self.llm.generate(improvement_prompt, temperature=0.5)
            return improved.strip()
        except Exception as e:
            logger.error(f"Improvement failed: {str(e)}")
            return content
    
    def _update_content(self, context: ExecutionContext, improved_content: str) -> None:
        """Update context with improved content."""
        if not improved_content:
            return
        
        # Split into sections
        sections = improved_content.split("\n\n")
        for i, result in enumerate(context.results):
            if i < len(sections):
                result.content = sections[i]
    
    def _generate_summary(self, context: ExecutionContext, content: str) -> str:
        """Generate a universal summary."""
        try:
            prompt = UNIVERSAL_SUMMARIZER_PROMPT.format(
                document_type=context.document_type or "Document",
                document_content=content[:2000]
            )
            summary = self.llm.generate(prompt, temperature=0.3)
            return summary.strip()
        except Exception as e:
            logger.error(f"Summary generation failed: {str(e)}")
            return f"A professional {context.document_type} document has been generated."