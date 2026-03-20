"""
GLITCH ORCHESTRATOR
The brain of the system - parses requests, breaks into tasks, assigns agents
"""

from typing import List, Dict, Any
from app.core.agent_manager import AgentManager
from app.core.task_engine import TaskEngine
from app.services.llm_service import LLMService
import asyncio


class Orchestrator:
    """
    Central orchestrator that coordinates all GLITCH operations.
    - Parses user requests using LLM
    - Creates execution plans
    - Assigns agents to tasks
    - Manages workflow
    """

    def __init__(self):
        self.agent_manager = AgentManager()
        self.task_engine = TaskEngine()
        self.llm = LLMService()
        self.active_projects = {}

    async def handle_request(self, user_input: str, project_id: str = None) -> Dict[str, Any]:
        """
        Main entry point for all GLITCH requests.
        """
        # Step 1: Analyze the request
        analysis = await self.analyze_request(user_input)

        # Step 2: Create task plan
        task_plan = await self.create_task_plan(analysis)

        # Step 3: Execute tasks with agents
        results = await self.execute_plan(task_plan, project_id)

        # Step 4: Merge and return results
        return self.compile_results(results, analysis)

    async def analyze_request(self, user_input: str) -> Dict[str, Any]:
        """
        Use LLM to understand what the user wants to build.
        """
        prompt = f"""
        Analyze this development request and extract:
        1. Project type (web app, mobile app, API, automation, etc.)
        2. Core features needed
        3. Tech stack suggestions
        4. Complexity level (simple, medium, complex)
        5. Required agents

        Request: {user_input}

        Return as structured analysis.
        """

        analysis = await self.llm.analyze(prompt)

        return {
            "raw_input": user_input,
            "project_type": analysis.get("project_type", "web_app"),
            "features": analysis.get("features", []),
            "tech_stack": analysis.get("tech_stack", {}),
            "complexity": analysis.get("complexity", "medium"),
            "required_agents": analysis.get("agents", ["architect", "fullstack_dev"])
        }

    async def create_task_plan(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Break down the project into executable tasks.
        """
        complexity = analysis.get("complexity", "medium")
        project_type = analysis.get("project_type", "web_app")

        # Base task templates
        task_templates = {
            "web_app": [
                {"phase": "architecture", "type": "design", "agent": "architect"},
                {"phase": "backend", "type": "development", "agent": "backend_dev"},
                {"phase": "frontend", "type": "development", "agent": "frontend_dev"},
                {"phase": "database", "type": "setup", "agent": "backend_dev"},
                {"phase": "integration", "type": "development", "agent": "fullstack_dev"},
                {"phase": "deployment", "type": "devops", "agent": "devops"},
            ],
            "mobile_app": [
                {"phase": "architecture", "type": "design", "agent": "architect"},
                {"phase": "ui_design", "type": "design", "agent": "uiux"},
                {"phase": "app_development", "type": "development", "agent": "mobile_dev"},
                {"phase": "api_integration", "type": "development", "agent": "backend_dev"},
                {"phase": "deployment", "type": "devops", "agent": "devops"},
            ],
            "api": [
                {"phase": "architecture", "type": "design", "agent": "architect"},
                {"phase": "api_development", "type": "development", "agent": "backend_dev"},
                {"phase": "documentation", "type": "docs", "agent": "backend_dev"},
                {"phase": "deployment", "type": "devops", "agent": "devops"},
            ],
            "automation": [
                {"phase": "workflow_design", "type": "design", "agent": "architect"},
                {"phase": "script_development", "type": "development", "agent": "ai_engineer"},
                {"phase": "integration", "type": "development", "agent": "devops"},
            ],
        }

        base_tasks = task_templates.get(project_type, task_templates["web_app"])

        # Enrich tasks with analysis context
        tasks = []
        for i, task in enumerate(base_tasks):
            tasks.append({
                "id": f"task_{i+1}",
                "phase": task["phase"],
                "type": task["type"],
                "agent": task["agent"],
                "context": analysis,
                "status": "pending",
                "dependencies": [f"task_{i}"] if i > 0 else [],
                "priority": i + 1
            })

        return tasks

    async def execute_plan(self, task_plan: List[Dict], project_id: str = None) -> List[Dict]:
        """
        Execute the task plan using assigned agents.
        """
        results = []

        for task in task_plan:
            # Get or spawn the required agent
            agent = await self.agent_manager.get_agent(task["agent"])

            # Add task to engine
            task_id = self.task_engine.add_task(task)

            # Execute task
            self.task_engine.update_status(task_id, "in_progress")

            try:
                result = await agent.execute(task)
                self.task_engine.update_status(task_id, "completed")
                results.append({
                    "task_id": task_id,
                    "phase": task["phase"],
                    "status": "completed",
                    "output": result
                })
            except Exception as e:
                self.task_engine.update_status(task_id, "failed")
                results.append({
                    "task_id": task_id,
                    "phase": task["phase"],
                    "status": "failed",
                    "error": str(e)
                })

        return results

    def compile_results(self, results: List[Dict], analysis: Dict) -> Dict[str, Any]:
        """
        Compile all results into final output.
        """
        completed = [r for r in results if r["status"] == "completed"]
        failed = [r for r in results if r["status"] == "failed"]

        # Extract code outputs
        code_outputs = {}
        for result in completed:
            if "output" in result and isinstance(result["output"], dict):
                if "code" in result["output"]:
                    code_outputs[result["phase"]] = result["output"]["code"]
                if "files" in result["output"]:
                    code_outputs[f"{result['phase']}_files"] = result["output"]["files"]

        return {
            "success": len(failed) == 0,
            "project_type": analysis.get("project_type"),
            "summary": {
                "total_tasks": len(results),
                "completed": len(completed),
                "failed": len(failed)
            },
            "phases_completed": [r["phase"] for r in completed],
            "code": code_outputs,
            "results": results
        }

    async def get_project_status(self, project_id: str) -> Dict[str, Any]:
        """
        Get current status of a project.
        """
        if project_id in self.active_projects:
            return self.active_projects[project_id]
        return {"error": "Project not found"}

    async def cancel_project(self, project_id: str) -> bool:
        """
        Cancel an active project.
        """
        if project_id in self.active_projects:
            # Kill all agents working on this project
            await self.agent_manager.kill_project_agents(project_id)
            del self.active_projects[project_id]
            return True
        return False
