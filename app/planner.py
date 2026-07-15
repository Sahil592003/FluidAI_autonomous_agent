
"""Universal planning module for any document type."""

import logging
import json
from typing import Dict, Any, List

from app.llm import GeminiLLM
from app.models import PlanningOutput
from app.prompts.prompts import UNIVERSAL_PLANNER_PROMPT

logger = logging.getLogger(__name__)


class Planner:
    """Universal planner that handles ANY document type."""
    
    def __init__(self, llm: GeminiLLM):
        self.llm = llm
        self.document_types = set()
    
    def create_plan(self, request: str) -> PlanningOutput:
        """
        Create an execution plan for ANY document request.
        
        Args:
            request: Natural language request
            
        Returns:
            PlanningOutput with document type, assumptions, and tasks
        """
        logger.info(f"Creating universal plan for: {request[:100]}...")
        
        try:
            # Generate the plan using LLM
            prompt = UNIVERSAL_PLANNER_PROMPT.format(request=request)
            plan_data = self.llm.generate_json(prompt)
            
            # Validate the response
            if not all(k in plan_data for k in ["document_type", "assumptions", "tasks"]):
                raise ValueError("Invalid plan structure from LLM")
            
            # Ensure tasks are reasonable
            tasks = plan_data["tasks"]
            if len(tasks) < 3:
                # Add default tasks if not enough
                logger.warning("Not enough tasks, adding defaults")
                tasks.extend([
                    "Task 1: Create executive summary",
                    "Task 2: Write introduction",
                    "Task 3: Define objectives"
                ])
            
            # Limit tasks to avoid rate limits
            if len(tasks) > 8:
                logger.info(f"Limiting tasks from {len(tasks)} to 8")
                tasks = tasks[:8]
            
            # Create the planning output
            plan = PlanningOutput(
                document_type=plan_data["document_type"],
                assumptions=plan_data["assumptions"],
                tasks=tasks
            )
            
            self.document_types.add(plan.document_type)
            logger.info(f"✅ Universal plan created: {plan.document_type} with {len(plan.tasks)} tasks")
            return plan
            
        except Exception as e:
            logger.error(f"Planning failed: {str(e)}")
            # Fallback to default plan
            return self._create_fallback_plan(request)
    
    def _create_fallback_plan(self, request: str) -> PlanningOutput:
        """Create a fallback plan if LLM fails."""
        logger.info("Creating fallback plan")
        
        return PlanningOutput(
            document_type="Professional Document",
            assumptions=[
                "The document follows standard professional structure",
                "Content is based on the user's request",
                "Formatting will be consistent with professional standards"
            ],
            tasks=[
                "Task 1: Create executive summary",
                "Task 2: Write introduction and context",
                "Task 3: Define objectives and scope",
                "Task 4: Describe solution or approach",
                "Task 5: Provide implementation details",
                "Task 6: Outline timeline and resources",
                "Task 7: Identify risks and mitigation",
                "Task 8: Write conclusion and next steps"
            ]
        )