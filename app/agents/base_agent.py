"""
GLITCH BASE AGENT
Foundation class for all specialized agents
"""

from typing import Dict, Any
from datetime import datetime
from app.services.llm_service import LLMService


class BaseAgent:
    """
    Base class for all GLITCH agents.
    Provides common functionality for AI-powered development agents.
    """

    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.name = self._get_agent_name()
        self.status = "idle"
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        self.current_task = None
        self.completed_tasks = []
        self.llm = LLMService()
        self.system_prompt = self._get_system_prompt()

    def _get_agent_name(self) -> str:
        """Get human-readable agent name."""
        names = {
            "architect": "System Architect",
            "ai_engineer": "AI Engineer",
            "fullstack_dev": "Full-Stack Developer",
            "backend_dev": "Backend Developer",
            "frontend_dev": "Frontend Developer",
            "devops": "DevOps Engineer",
            "uiux": "UI/UX Designer",
            "mobile_dev": "Mobile Developer",
        }
        return names.get(self.agent_type, "Developer")

    def _get_system_prompt(self) -> str:
        """Get agent-specific system prompt - override in subclasses."""
        return f"""You are {self.name}, an expert {self.agent_type} working in the GLITCH AI development system.

Your role is to:
- Analyze requirements carefully
- Write clean, production-ready code
- Follow best practices for your domain
- Provide clear explanations of your decisions

Always output structured responses with code blocks when generating code."""

    async def execute(self, task: Dict) -> Dict[str, Any]:
        """
        Execute a task - main entry point.
        """
        self.status = "working"
        self.current_task = task
        self.last_active = datetime.now()

        try:
            result = await self._process_task(task)
            self.completed_tasks.append(task.get("id"))
            return result
        finally:
            self.status = "idle"
            self.current_task = None

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        """
        Process the task - override in subclasses for specialized behavior.
        """
        phase = task.get("phase", "development")
        context = task.get("context", {})

        prompt = self._build_prompt(phase, context)
        response = await self.llm.generate(prompt, self.system_prompt)

        return self._parse_response(response, phase)

    def _build_prompt(self, phase: str, context: Dict) -> str:
        """
        Build a prompt for the LLM based on task phase and context.
        """
        project_type = context.get("project_type", "application")
        features = context.get("features", [])
        tech_stack = context.get("tech_stack", {})

        return f"""
Task Phase: {phase}
Project Type: {project_type}
Features Required: {', '.join(features) if features else 'General features'}
Tech Stack: {tech_stack}

Please complete this {phase} phase by providing:
1. Clear implementation plan
2. Required code/configurations
3. Any necessary explanations

Focus on production-quality output.
"""

    def _parse_response(self, response: str, phase: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured output.
        """
        # Extract code blocks if present
        code_blocks = []
        lines = response.split('\n')
        in_code_block = False
        current_block = []
        current_lang = ""

        for line in lines:
            if line.startswith('```'):
                if in_code_block:
                    code_blocks.append({
                        "language": current_lang,
                        "code": '\n'.join(current_block)
                    })
                    current_block = []
                    in_code_block = False
                else:
                    in_code_block = True
                    current_lang = line[3:].strip() or "text"
            elif in_code_block:
                current_block.append(line)

        return {
            "phase": phase,
            "explanation": response,
            "code_blocks": code_blocks,
            "files": self._extract_files(code_blocks)
        }

    def _extract_files(self, code_blocks: list) -> Dict[str, str]:
        """
        Extract file contents from code blocks.
        """
        files = {}
        lang_extensions = {
            "python": ".py",
            "javascript": ".js",
            "typescript": ".ts",
            "jsx": ".jsx",
            "tsx": ".tsx",
            "html": ".html",
            "css": ".css",
            "json": ".json",
            "yaml": ".yaml",
            "sql": ".sql",
            "bash": ".sh",
        }

        for i, block in enumerate(code_blocks):
            lang = block.get("language", "text")
            ext = lang_extensions.get(lang, ".txt")
            filename = f"output_{i+1}{ext}"
            files[filename] = block.get("code", "")

        return files

    def update_status(self, status: str):
        """Update agent status."""
        self.status = status
        self.last_active = datetime.now()

    def get_info(self) -> Dict:
        """Get agent information."""
        return {
            "id": self.agent_id,
            "type": self.agent_type,
            "name": self.name,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "completed_tasks": len(self.completed_tasks)
        }
