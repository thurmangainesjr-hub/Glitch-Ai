"""
GLITCH FRONTEND DEVELOPER AGENT
UI/UX implementation specialist
"""

from app.agents.base_agent import BaseAgent
from typing import Dict, Any


class FrontendDevAgent(BaseAgent):
    """
    Frontend Developer Agent - builds beautiful,
    responsive user interfaces.
    """

    def _get_system_prompt(self) -> str:
        return """You are a Senior Frontend Developer for GLITCH.

Your expertise includes:
- Frameworks: React, Next.js, Vue, Svelte
- Styling: Tailwind CSS, CSS Modules, Styled Components
- State: Redux, Zustand, Recoil, Context
- Animation: Framer Motion, GSAP
- Forms: React Hook Form, Formik
- Data Fetching: React Query, SWR, Axios
- Testing: Jest, React Testing Library, Cypress

You create:
1. Responsive, accessible interfaces
2. Reusable component libraries
3. Smooth animations and transitions
4. Optimized performance
5. Clean component architecture

Design principles:
- Mobile-first responsive design
- Accessibility (WCAG compliance)
- Performance optimization
- Clean, maintainable code"""

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        context = task.get("context", {})

        prompt = f"""
Build frontend implementation for:

Project: {context.get('project_type', 'application')}
Features: {context.get('features', [])}
Style: Modern, professional, responsive

Generate:
1. Page components
2. Reusable UI components
3. Styling (Tailwind CSS)
4. State management
5. API integration hooks
"""

        response = await self.llm.generate(prompt, self.system_prompt)
        return self._parse_response(response, "frontend")
