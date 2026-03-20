"""
GLITCH TECH LEAD AGENT
Technical leadership and code review specialist
"""

from app.agents.base_agent import BaseAgent
from typing import Dict, Any


class TechLeadAgent(BaseAgent):
    """
    Tech Lead Agent - provides technical guidance,
    code reviews, and architectural decisions.
    """

    def _get_system_prompt(self) -> str:
        return """You are the Tech Lead for GLITCH.

Your expertise includes:
- Technical strategy and decision-making
- Code review and quality standards
- Architecture review and validation
- Team mentorship and guidance
- Technical debt management
- Performance optimization
- Cross-team coordination

You provide:
1. Technical direction
2. Code review feedback
3. Architecture validation
4. Best practice enforcement
5. Risk assessment
6. Technical documentation
7. Implementation guidance

Leadership principles:
- Pragmatic decisions
- Team enablement
- Quality focus
- Clear communication
- Continuous improvement"""

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        context = task.get("context", {})

        prompt = f"""
Review and provide technical guidance for:

Project: {context.get('project_type', 'application')}
Features: {context.get('features', [])}
Phase: {task.get('phase', 'review')}

Provide:
1. Architecture review
2. Code quality assessment
3. Best practice recommendations
4. Risk analysis
5. Technical roadmap
6. Implementation priorities
"""

        response = await self.llm.generate(prompt, self.system_prompt)
        return self._parse_response(response, "review")
