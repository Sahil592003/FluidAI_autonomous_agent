
"""FastAPI application for the FluidAI agent."""

import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import Config
from app.models import AgentRequest, AgentResponse
from app.agent import Agent

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Validate configuration
try:
    Config.validate()
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

# Initialize agent
agent = Agent()

# Create FastAPI app
app = FastAPI(
    title="FluidAI - Autonomous AI Agent",
    description="Autonomous AI Agent for document generation using Gemini",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {
        "service": "FluidAI",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/agent", response_model=AgentResponse)
async def process_agent_request(request: AgentRequest):
    """
    Process a natural language request and generate a document.
    
    Args:
        request: AgentRequest with the user's request
        
    Returns:
        AgentResponse with the results
    """
    logger.info(f"Received agent request: {request.request[:100]}...")
    
    try:
        # Process the request
        response = agent.process_request(request)
        
        # Log the response
        logger.info(f"Request processed: {response.status} in {response.execution_time}")
        
        if response.status == "failed":
            # Check if it's a rate limit error
            if response.error and ("429" in response.error or "rate limit" in response.error.lower()):
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content=response.dict()
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=response.error or "Processing failed"
                )
        
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        
        # Check if it's a rate limit error
        if "429" in str(e) or "quota" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please wait 30-60 seconds and try again."
            )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with proper response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=Config.DEBUG
    )