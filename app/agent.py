
"""Universal autonomous agent with batch execution."""

import logging
import time
from datetime import datetime

from app.llm import GeminiLLM
from app.models import AgentRequest, AgentResponse, ExecutionContext
from app.planner import Planner
from app.batch_executor import BatchExecutor
from app.reflection import Reflection
from app.doc_generator import DocumentGenerator

logger = logging.getLogger(__name__)


class Agent:
    """Universal autonomous agent with optimized API usage."""
    
    def __init__(self):
        """Initialize the universal agent."""
        self.llm = GeminiLLM()
        self.planner = Planner(self.llm)
        self.executor = BatchExecutor(self.llm)
        self.reflection = Reflection(self.llm)
        self.doc_generator = DocumentGenerator()
        self.last_request_time = 0
        self.min_interval = 10
    
    def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process ANY document request with minimal API calls."""
        
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_interval and self.last_request_time > 0:
            wait_time = self.min_interval - time_since_last
            logger.info(f"⏳ Waiting {wait_time:.1f}s before processing...")
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
        start_time = datetime.now()
        
        logger.info(f"🚀 Processing: {request.request[:100]}...")
        
        context = ExecutionContext(
            request=request.request,
            start_time=start_time,
            status="pending"
        )
        
        try:
            # Phase 1: Planning (1 API call)
            logger.info("📋 Phase 1: Planning")
            plan = self.planner.create_plan(request.request)
            context.document_type = plan.document_type
            context.assumptions = plan.assumptions
            context.tasks = plan.tasks
            logger.info(f"✅ Plan: {plan.document_type} with {len(plan.tasks)} tasks")
            
            # Phase 2: Batch Execution (1 API call)
            logger.info("⚡ Phase 2: Batch Execution (ALL sections in 1 call)")
            context = self.executor.execute_tasks(context)
            
            if context.status == "failed":
                return self._create_error_response(context)
            
            # Phase 3: Reflection (1 API call)
            logger.info("🔍 Phase 3: Reflection")
            context = self.reflection.reflect(context)
            
            # Phase 4: Document Generation (0 API calls)
            logger.info("📄 Phase 4: Document Generation")
            context.document_path = self.doc_generator.generate(context)
            
            context.status = "completed"
            context.end_time = datetime.now()
            
            execution_time = (context.end_time - context.start_time).total_seconds()
            logger.info(f"✅ Completed in {execution_time:.1f}s with only 3-4 API calls!")
            
            return self._create_response(context)
            
        except Exception as e:
            logger.error(f"❌ Agent failed: {str(e)}")
            context.status = "failed"
            context.error = str(e)
            context.end_time = datetime.now()
            return self._create_error_response(context)
    
    def _create_response(self, context: ExecutionContext) -> AgentResponse:
        """Create success response."""
        execution_time = (context.end_time - context.start_time).total_seconds()
        
        return AgentResponse(
            status="success",
            execution_time=f"{execution_time:.1f} sec",
            plan=context.plan,
            assumptions=context.assumptions,
            document_path=context.document_path or "",
            summary=context.summary or f"Professional {context.document_type} generated"
        )
    
    def _create_error_response(self, context: ExecutionContext) -> AgentResponse:
        """Create error response."""
        execution_time = (context.end_time - context.start_time).total_seconds() if context.end_time else 0
        
        return AgentResponse(
            status="failed",
            execution_time=f"{execution_time:.1f} sec",
            plan=context.plan or [],
            assumptions=context.assumptions or [],
            document_path="",
            summary="",
            error=context.error or "Unknown error occurred"
        )