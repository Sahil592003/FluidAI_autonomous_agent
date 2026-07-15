
"""Enhanced Pydantic models for universal agent."""

from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    """Universal request model."""
    request: str = Field(..., min_length=1, description="Natural language request for ANY document type")


class PlanningOutput(BaseModel):
    """Universal planning output."""
    document_type: str = Field(..., description="Type of document to generate")
    assumptions: List[str] = Field(..., description="List of assumptions made")
    tasks: List[str] = Field(..., description="List of tasks to execute in order")


class TaskResult(BaseModel):
    """Result of a single task execution."""
    task: str
    content: str
    status: str
    error: Optional[str] = None
    execution_time: float


class AgentResponse(BaseModel):
    """Universal response model."""
    status: str
    execution_time: str
    plan: List[str]
    assumptions: List[str]
    document_path: str
    summary: str
    error: Optional[str] = None


class ExecutionContext(BaseModel):
    """Universal execution context."""
    request: str
    document_type: Optional[str] = None
    assumptions: List[str] = []
    tasks: List[str] = []
    results: List[TaskResult] = []
    plan: List[str] = []
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    document_path: Optional[str] = None
    summary: Optional[str] = None
    status: str = "pending"
    error: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True