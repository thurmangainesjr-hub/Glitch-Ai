"""
GLITCH FULLSTACK DEVELOPER AGENT
End-to-end application development
"""

from app.agents.base_agent import BaseAgent
from typing import Dict, Any


class FullstackDevAgent(BaseAgent):
    """
    Full-Stack Developer Agent - builds complete applications
    from frontend to backend.
    """

    def _get_system_prompt(self) -> str:
        return """You are a Senior Full-Stack Developer for GLITCH.

Your expertise includes:
- Frontend: React, Next.js, Vue, Tailwind CSS
- Backend: Node.js, Python (FastAPI/Django), Express
- Databases: PostgreSQL, MongoDB, Redis
- APIs: REST, GraphQL
- Authentication: JWT, OAuth, sessions
- Real-time: WebSockets, Server-Sent Events

When building features, you:
1. Write clean, maintainable code
2. Follow best practices and patterns
3. Implement proper error handling
4. Add appropriate comments
5. Consider security implications
6. Optimize for performance

Output production-ready code with proper structure."""

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        context = task.get("context", {})
        phase = task.get("phase", "development")

        prompt = f"""
Build {phase} implementation for:

Project: {context.get('project_type', 'web application')}
Features: {context.get('features', [])}
Tech Stack: {context.get('tech_stack', {})}

Requirements:
- Production-ready code
- Proper error handling
- Clean file structure
- Database integration
- API endpoints

Generate complete, working code files.
"""

        response = await self.llm.generate(prompt, self.system_prompt)
        return self._parse_response(response, phase)
