"""
GLITCH BUILD ROUTES
Main execution endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
from app.core.orchestrator import Orchestrator
from app.models.project import BuildRequest, BuildResponse
import uuid

router = APIRouter(prefix="/build", tags=["build"])

# Global orchestrator instance
orchestrator = Orchestrator()


@router.post("/execute", response_model=BuildResponse)
async def execute_build(request: BuildRequest):
    """
    Execute a build request.
    Main entry point for GLITCH development.
    """
    try:
        project_id = request.project_id or f"project_{uuid.uuid4().hex[:8]}"

        result = await orchestrator.handle_request(
            user_input=request.input,
            project_id=project_id
        )

        return BuildResponse(
            success=result.get("success", False),
            project_id=project_id,
            summary=result.get("summary", {}),
            phases_completed=result.get("phases_completed", []),
            code=result.get("code", {}),
            results=result.get("results", [])
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quick")
async def quick_build(payload: Dict[str, Any]):
    """
    Quick build endpoint for simple requests.
    """
    user_input = payload.get("input", "")
    if not user_input:
        raise HTTPException(status_code=400, detail="Input required")

    result = await orchestrator.handle_request(user_input)
    return result


@router.get("/status/{project_id}")
async def get_build_status(project_id: str):
    """
    Get the status of a build/project.
    """
    status = await orchestrator.get_project_status(project_id)
    if "error" in status:
        raise HTTPException(status_code=404, detail=status["error"])
    return status


@router.post("/cancel/{project_id}")
async def cancel_build(project_id: str):
    """
    Cancel an active build.
    """
    success = await orchestrator.cancel_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"success": True, "message": f"Project {project_id} cancelled"}
