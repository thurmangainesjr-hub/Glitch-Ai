"""
GLITCH TASK MODEL
Task data structures
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(str, Enum):
    DESIGN = "design"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    DOCUMENTATION = "documentation"


class TaskCreate(BaseModel):
    """Request model for creating a task."""
    phase: str
    type: TaskType
    agent: str
    context: Dict = Field(default_factory=dict)
    priority: int = 5
    dependencies: List[str] = Field(default_factory=list)


class TaskResponse(BaseModel):
    """Response model for task data."""
    id: str
    phase: str
    type: TaskType
    agent: str
    status: TaskStatus
    progress: int
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    result: Optional[Dict]
    error: Optional[str]


class TaskProgress(BaseModel):
    """Model for task progress updates."""
    task_id: str
    progress: int
    status: Optional[TaskStatus]
    message: Optional[str]
