"""
GLITCH AGENTS ROUTES
Agent management endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List
from app.core.agent_manager import AgentManager
from app.models.agent import AgentInfo, AgentPoolStatus, AgentRequest, AgentType

router = APIRouter(prefix="/agents", tags=["agents"])

# Global agent manager
agent_manager = AgentManager()


@router.get("/", response_model=AgentPoolStatus)
async def get_agents_status():
    """
    Get status of all agents.
    """
    return agent_manager.get_status()


@router.get("/types")
async def get_agent_types():
    """
    Get all available agent types.
    """
    return {
        "types": [
            {
                "id": "architect",
                "name": "System Architect",
                "description": "Designs system architecture and tech stack"
            },
            {
                "id": "ai_engineer",
                "name": "AI Engineer",
                "description": "AI integrations and automation"
            },
            {
                "id": "fullstack_dev",
                "name": "Full-Stack Developer",
                "description": "End-to-end application development"
            },
            {
                "id": "backend_dev",
                "name": "Backend Developer",
                "description": "APIs, databases, server logic"
            },
            {
                "id": "frontend_dev",
                "name": "Frontend Developer",
                "description": "UI/UX implementation"
            },
            {
                "id": "mobile_dev",
                "name": "Mobile Developer",
                "description": "iOS, Android, cross-platform apps"
            },
            {
                "id": "devops",
                "name": "DevOps Engineer",
                "description": "CI/CD, deployment, infrastructure"
            },
            {
                "id": "uiux",
                "name": "UI/UX Designer",
                "description": "Design systems and user experience"
            },
            {
                "id": "qa_engineer",
                "name": "QA Engineer",
                "description": "Testing and quality assurance"
            },
            {
                "id": "security_engineer",
                "name": "Security Engineer",
                "description": "Security implementation and auditing"
            },
            {
                "id": "data_engineer",
                "name": "Data Engineer",
                "description": "Data pipelines and analytics"
            },
            {
                "id": "tech_lead",
                "name": "Tech Lead",
                "description": "Technical guidance and code review"
            },
            {
                "id": "product_manager",
                "name": "Product Manager",
                "description": "Requirements and product strategy"
            }
        ]
    }


@router.post("/spawn/{agent_type}")
async def spawn_agent(agent_type: str):
    """
    Spawn a new agent of the specified type.
    """
    try:
        agent = await agent_manager.spawn_agent(agent_type)
        return {
            "success": True,
            "agent": agent.get_info()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{agent_id}")
async def kill_agent(agent_id: str):
    """
    Kill a specific agent.
    """
    await agent_manager.kill_agent(agent_id)
    return {"success": True, "message": f"Agent {agent_id} terminated"}


@router.post("/cleanup")
async def cleanup_idle_agents():
    """
    Kill all idle agents.
    """
    killed = await agent_manager.kill_idle_agents()
    return {
        "success": True,
        "message": f"Killed {killed} idle agents"
    }
