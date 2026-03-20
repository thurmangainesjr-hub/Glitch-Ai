"""
GLITCH UI/UX DESIGNER AGENT
Design system and user experience specialist
"""

from app.agents.base_agent import BaseAgent
from typing import Dict, Any


class UIUXAgent(BaseAgent):
    """
    UI/UX Designer Agent - creates design systems,
    user flows, and visual designs.
    """

    def _get_system_prompt(self) -> str:
        return """You are a Senior UI/UX Designer for GLITCH.

Your expertise includes:
- Design Systems: Component libraries, tokens, guidelines
- Visual Design: Color theory, typography, spacing
- User Research: Personas, user flows, wireframes
- Prototyping: Figma, Sketch, Adobe XD
- Accessibility: WCAG, color contrast, screen readers
- Animation: Micro-interactions, transitions
- Mobile: iOS HIG, Material Design

You create:
1. Design system specifications
2. Component design guidelines
3. Color palettes and themes
4. Typography scales
5. Spacing systems
6. User flow diagrams
7. Wireframes and mockups

Output includes:
- Tailwind CSS configurations
- CSS custom properties
- Component specifications
- Design tokens (JSON)"""

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        context = task.get("context", {})

        prompt = f"""
Create UI/UX design system for:

Project: {context.get('project_type', 'application')}
Style: Modern, professional, accessible
Theme: Dark mode with accent colors

Generate:
1. Color palette (hex codes)
2. Typography scale
3. Spacing system
4. Component specifications
5. Tailwind config
6. CSS variables
7. Design tokens JSON
"""

        response = await self.llm.generate(prompt, self.system_prompt)
        return self._parse_response(response, "design")
