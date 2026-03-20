"""
GLITCH PROJECT MODEL
Project data structures
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class ProjectStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProjectType(str, Enum):
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    API = "api"
    AUTOMATION = "automation"
    OTHER = "other"


class ProjectCreate(BaseModel):
    """Request model for creating a project."""
    input: str = Field(..., description="User's project description")
    name: Optional[str] = Field(None, description="Project name")


class ProjectResponse(BaseModel):
    """Response model for project data."""
    id: str
    name: str
    description: str
    project_type: ProjectType
    status: ProjectStatus
    features: List[str]
    tech_stack: Dict[str, str]
    created_at: datetime
    updated_at: Optional[datetime]


class BuildRequest(BaseModel):
    """Request model for building a project."""
    input: str = Field(..., description="What to build")
    project_id: Optional[str] = Field(None, description="Existing project ID")
    options: Optional[Dict] = Field(default_factory=dict)


class BuildResponse(BaseModel):
    """Response model for build results."""
    success: bool
    project_id: str
    summary: Dict
    phases_completed: List[str]
    code: Dict[str, str]
    results: List[Dict]
