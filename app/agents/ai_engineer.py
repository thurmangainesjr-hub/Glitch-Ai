"""
GLITCH AI ENGINEER AGENT
AI/ML integration and automation specialist
"""

from app.agents.base_agent import BaseAgent
from typing import Dict, Any


class AIEngineerAgent(BaseAgent):
    """
    AI Engineer Agent - handles AI integrations,
    prompt engineering, and automation workflows.
    """

    def _get_system_prompt(self) -> str:
        return """You are the AI Engineer for GLITCH, specializing in AI-powered systems.

Your expertise includes:
- LLM integration (OpenAI, Anthropic, local models)
- Prompt engineering and optimization
- AI agent design and orchestration
- Vector databases and RAG systems
- Automation workflows (n8n, Zapier, custom)
- ML model deployment and monitoring

When given a task, you will:
1. Design AI-powered solutions
2. Create optimized prompts
3. Build agent workflows
4. Implement AI integrations
5. Set up automation pipelines

Output clean, production-ready code with proper error handling."""

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        context = task.get("context", {})

        prompt = f"""
Create AI/automation implementation for:

Project: {context.get('project_type', 'application')}
Features: {context.get('features', [])}
Request: {context.get('raw_input', 'Build AI features')}

Provide:
1. AI integration architecture
2. Prompt templates
3. Agent workflow design
4. Implementation code
5. API endpoints for AI features
"""

        response = await self.llm.generate(prompt, self.system_prompt)
        return self._parse_response(response, "ai_integration")
