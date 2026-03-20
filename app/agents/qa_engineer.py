"""
GLITCH QA ENGINEER AGENT
Testing and quality assurance specialist
"""

from app.agents.base_agent import BaseAgent
from typing import Dict, Any


class QAEngineerAgent(BaseAgent):
    """
    QA Engineer Agent - writes tests, performs
    quality assurance, and ensures reliability.
    """

    def _get_system_prompt(self) -> str:
        return """You are a Senior QA Engineer for GLITCH.

Your expertise includes:
- Unit Testing: Jest, Pytest, Vitest
- Integration Testing: Supertest, TestClient
- E2E Testing: Cypress, Playwright, Selenium
- API Testing: Postman, Insomnia, REST Client
- Performance: k6, Artillery, Lighthouse
- Security: OWASP, penetration testing
- Accessibility: axe, WAVE

You create:
1. Unit test suites
2. Integration tests
3. E2E test scenarios
4. API test collections
5. Performance benchmarks
6. Security scan configs
7. Test automation pipelines

Testing principles:
- Test coverage > 80%
- Fast, reliable tests
- CI/CD integration
- Clear test documentation"""

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        context = task.get("context", {})

        prompt = f"""
Create comprehensive test suite for:

Project: {context.get('project_type', 'application')}
Features: {context.get('features', [])}

Generate:
1. Unit tests (Jest/Pytest)
2. Integration tests
3. E2E test scenarios
4. API test collection
5. Test configuration
"""

        response = await self.llm.generate(prompt, self.system_prompt)
        return self._parse_response(response, "testing")
