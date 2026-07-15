
"""Universal executor for any document type."""

import logging
import time
from typing import Dict, Any

from app.llm import GeminiLLM
from app.models import TaskResult, ExecutionContext
from app.prompts.prompts import UNIVERSAL_EXECUTOR_PROMPT, UNIVERSAL_SECTION_TEMPLATES

logger = logging.getLogger(__name__)


class Executor:
    """Universal executor that handles ANY document type."""
    
    def __init__(self, llm: GeminiLLM):
        self.llm = llm
        self.min_delay = 25
        self.max_retries = 5
    
    def execute_tasks(self, context: ExecutionContext) -> ExecutionContext:
        """Execute all tasks for ANY document type."""
        logger.info(f"Universal execution of {len(context.tasks)} tasks")
        
        full_content = ""
        section_contents = {}
        
        for i, task in enumerate(context.tasks, 1):
            logger.info(f"Executing task {i}/{len(context.tasks)}: {task}")
            
            if i > 1:
                logger.info(f"Waiting {self.min_delay}s for rate limits...")
                time.sleep(self.min_delay)
            
            start_time = time.time()
            try:
                content = self._execute_task(context, task, full_content)
                
                task_result = TaskResult(
                    task=task,
                    content=content,
                    status="completed",
                    execution_time=time.time() - start_time
                )
                context.results.append(task_result)
                
                if content:
                    full_content += f"\n\n{content}"
                    section_contents[task] = content
                
                logger.info(f"Task {i} completed in {task_result.execution_time:.2f}s")
                
            except Exception as e:
                logger.error(f"Task {i} failed: {str(e)}")
                context.status = "failed"
                context.error = f"Task {i} failed: {str(e)}"
                break
        
        context.plan = context.tasks
        return context
    
    def _execute_task(self, context: ExecutionContext, task: str, previous_content: str) -> str:
        """Execute a single task for ANY document type."""
        # Extract section name
        section_name = task.split(":", 1)[-1].strip() if ":" in task else task
        
        # Determine document type
        doc_type = context.document_type or "Document"
        
        # Build context
        context_info = {
            "document_type": doc_type,
            "section_name": section_name,
            "context": f"Creating content for the '{section_name}' section of a {doc_type}",
            "previous_content": previous_content[:1000] if previous_content else "No previous content"
        }
        
        prompt = UNIVERSAL_EXECUTOR_PROMPT.format(**context_info)
        content = self.llm.generate(prompt, temperature=0.7)
        
        return content.strip()