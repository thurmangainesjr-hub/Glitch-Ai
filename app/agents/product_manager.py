"""
GLITCH PRODUCT MANAGER AGENT
Product strategy and requirements specialist
"""

from app.agents.base_agent import BaseAgent
from typing import Dict, Any


class ProductManagerAgent(BaseAgent):
    """
    Product Manager Agent - defines requirements,
    user stories, and product roadmap.
    """

    def _get_system_prompt(self) -> str:
        return """You are the Product Manager for GLITCH.

Your expertise includes:
- Requirements gathering and analysis
- User story creation
- Product roadmap planning
- Feature prioritization (RICE, MoSCoW)
- Market and competitive analysis
- User research and personas
- Metrics and KPIs definition
- Stakeholder management

You create:
1. Product requirements documents
2. User stories with acceptance criteria
3. Feature specifications
4. Product roadmaps
5. Success metrics
6. User personas
7. Competitive analysis

Product principles:
- User-centric design
- Data-driven decisions
- Iterative development
- Clear communication
- Value delivery focus"""

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        context = task.get("context", {})

        prompt = f"""
Define product requirements for:

Project: {context.get('project_type', 'application')}
Raw Request: {context.get('raw_input', 'Build an application')}

Generate:
1. Product overview
2. User personas
3. Feature list with priorities
4. User stories with acceptance criteria
5. Success metrics
6. MVP scope definition
7. Future roadmap ideas
"""

        response = await self.llm.generate(prompt, self.system_prompt)
        return self._parse_response(response, "product")
