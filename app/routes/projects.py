"""
GLITCH PROJECTS ROUTES
Project management endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.services.memory_service import MemoryService
from app.models.project import ProjectCreate, ProjectResponse
import uuid

router = APIRouter(prefix="/projects", tags=["projects"])

# Global memory service
memory = MemoryService()


@router.get("/")
async def list_projects():
    """
    List all projects.
    """
    projects = memory.list_projects()
    return {"projects": projects, "total": len(projects)}


@router.post("/")
async def create_project(request: ProjectCreate):
    """
    Create a new project.
    """
    project_id = f"project_{uuid.uuid4().hex[:8]}"

    project = memory.create_project(project_id, {
        "name": request.name or f"Project {project_id}",
        "description": request.input,
        "status": "pending"
    })

    return {"success": True, "project": project}


@router.get("/{project_id}")
async def get_project(project_id: str):
    """
    Get a specific project.
    """
    project = memory.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}")
async def update_project(project_id: str, updates: Dict[str, Any]):
    """
    Update a project.
    """
    project = memory.update_project(project_id, updates)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"success": True, "project": project}


@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """
    Delete a project.
    """
    success = memory.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"success": True, "message": f"Project {project_id} deleted"}


@router.get("/{project_id}/decisions")
async def get_project_decisions(project_id: str):
    """
    Get all decisions for a project.
    """
    decisions = memory.get_project_decisions(project_id)
    return {"decisions": decisions}


@router.get("/search/{query}")
async def search_projects(query: str):
    """
    Search projects.
    """
    results = memory.search_projects(query)
    return {"results": results, "total": len(results)}
