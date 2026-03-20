"""
GLITCH SECURITY ENGINEER AGENT
Application security and hardening specialist
"""

from app.agents.base_agent import BaseAgent
from typing import Dict, Any


class SecurityEngineerAgent(BaseAgent):
    """
    Security Engineer Agent - handles security
    audits, hardening, and secure coding.
    """

    def _get_system_prompt(self) -> str:
        return """You are a Senior Security Engineer for GLITCH.

Your expertise includes:
- OWASP Top 10 prevention
- Authentication: OAuth2, JWT, MFA
- Authorization: RBAC, ABAC, policies
- Cryptography: encryption, hashing, signing
- API Security: rate limiting, input validation
- Infrastructure: firewalls, WAF, secrets
- Compliance: GDPR, SOC2, HIPAA
- Scanning: SAST, DAST, dependency audit

You implement:
1. Secure authentication flows
2. Authorization systems
3. Input validation
4. Output encoding
5. Security headers
6. Secrets management
7. Audit logging
8. Security scanning configs

Always consider:
- Defense in depth
- Least privilege
- Zero trust
- Secure by default"""

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        context = task.get("context", {})

        prompt = f"""
Implement security for:

Project: {context.get('project_type', 'application')}
Features: {context.get('features', [])}

Generate:
1. Authentication implementation
2. Authorization middleware
3. Input validation schemas
4. Security headers config
5. Rate limiting
6. Audit logging
7. Security best practices checklist
"""

        response = await self.llm.generate(prompt, self.system_prompt)
        return self._parse_response(response, "security")
