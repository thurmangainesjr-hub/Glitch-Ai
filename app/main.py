"""
GLITCH - AI Development Orchestration System
Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import build, agents, projects
from app.core.orchestrator import Orchestrator
import os


# Lifespan for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║     ██████╗ ██╗     ██╗████████╗ ██████╗██╗  ██╗         ║
    ║    ██╔════╝ ██║     ██║╚══██╔══╝██╔════╝██║  ██║         ║
    ║    ██║  ███╗██║     ██║   ██║   ██║     ███████║         ║
    ║    ██║   ██║██║     ██║   ██║   ██║     ██╔══██║         ║
    ║    ╚██████╔╝███████╗██║   ██║   ╚██████╗██║  ██║         ║
    ║     ╚═════╝ ╚══════╝╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝         ║
    ║                                                           ║
    ║        AI Development Orchestration System                ║
    ║        EOF Ecosystem - Super Dev Team                     ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    print("🚀 GLITCH is starting up...")
    print("📡 API ready at http://localhost:8000")
    print("📚 Docs at http://localhost:8000/docs")
    yield
    # Shutdown
    print("👋 GLITCH shutting down...")


# Create FastAPI app
app = FastAPI(
    title="GLITCH",
    description="""
    ## AI Development Orchestration System

    GLITCH is a multi-agent AI system that builds software autonomously.

    ### Features
    - 🤖 **13 Specialized AI Agents** - From architects to security engineers
    - 🔄 **Task Orchestration** - Automatic task breakdown and execution
    - 📦 **Project Memory** - Persistent storage of projects and decisions
    - ⚡ **Parallel Execution** - Multiple agents working simultaneously

    ### Super Dev Team
    - System Architect
    - AI Engineer
    - Full-Stack Developer
    - Backend Developer
    - Frontend Developer
    - Mobile Developer
    - DevOps Engineer
    - UI/UX Designer
    - QA Engineer
    - Security Engineer
    - Data Engineer
    - Tech Lead
    - Product Manager
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(build.router, prefix="/api")
app.include_router(agents.router, prefix="/api")
app.include_router(projects.router, prefix="/api")

# Global orchestrator
glitch = Orchestrator()


@app.get("/")
async def root():
    """
    Root endpoint - system info.
    """
    return {
        "name": "GLITCH",
        "version": "1.0.0",
        "description": "AI Development Orchestration System",
        "status": "online",
        "endpoints": {
            "execute": "/api/build/execute",
            "agents": "/api/agents",
            "projects": "/api/projects",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "glitch"}


@app.post("/execute")
async def quick_execute(payload: dict):
    """
    Quick execution endpoint.
    Send {"input": "your request"} to build.
    """
    user_input = payload.get("input", "")
    if not user_input:
        raise HTTPException(status_code=400, detail="Input required")

    result = await glitch.handle_request(user_input)
    return {"result": result}


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return {
        "error": True,
        "message": str(exc),
        "type": type(exc).__name__
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
