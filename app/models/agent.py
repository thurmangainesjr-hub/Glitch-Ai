"""
GLITCH AGENT MODEL
Agent data structures
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class AgentType(str, Enum):
    ARCHITECT = "architect"
    AI_ENGINEER = "ai_engineer"
    FULLSTACK_DEV = "fullstack_dev"
    BACKEND_DEV = "backend_dev"
    FRONTEND_DEV = "frontend_dev"
    MOBILE_DEV = "mobile_dev"
    DEVOPS = "devops"
    UIUX = "uiux"
    QA_ENGINEER = "qa_engineer"
    SECURITY_ENGINEER = "security_engineer"
    DATA_ENGINEER = "data_engineer"
    TECH_LEAD = "tech_lead"
    PRODUCT_MANAGER = "product_manager"


class AgentStatus(str, Enum):
    IDLE = "idle"
    ASSIGNED = "assigned"
    WORKING = "working"
    ERROR = "error"


class AgentInfo(BaseModel):
    """Response model for agent information."""
    id: str
    type: AgentType
    name: str
    status: AgentStatus
    created_at: datetime
    last_active: datetime
    completed_tasks: int
    current_task: Optional[str]


class AgentPoolStatus(BaseModel):
    """Response model for agent pool status."""
    total_agents: int
    by_type: Dict[str, Dict]
    by_status: Dict[str, int]


class AgentRequest(BaseModel):
    """Request model for agent operations."""
    agent_type: AgentType
    action: str = "spawn"  # spawn, kill, assign
    task_id: Optional[str] = None
