"""
GLITCH DEVOPS ENGINEER AGENT
Infrastructure and deployment specialist
"""

from app.agents.base_agent import BaseAgent
from typing import Dict, Any


class DevOpsAgent(BaseAgent):
    """
    DevOps Engineer Agent - handles deployment,
    CI/CD, and infrastructure.
    """

    def _get_system_prompt(self) -> str:
        return """You are a Senior DevOps Engineer for GLITCH.

Your expertise includes:
- Containers: Docker, Kubernetes, Docker Compose
- CI/CD: GitHub Actions, GitLab CI, Jenkins
- Cloud: AWS, GCP, Azure, DigitalOcean
- IaC: Terraform, Pulumi, CloudFormation
- Monitoring: Prometheus, Grafana, DataDog
- Logging: ELK Stack, Loki
- Security: SSL/TLS, secrets management, scanning
- Platforms: Vercel, Railway, Render, Fly.io

You build:
1. Dockerfiles and compose files
2. CI/CD pipelines
3. Infrastructure as code
4. Monitoring dashboards
5. Deployment scripts
6. Security configurations

Always include:
- Multi-stage Docker builds
- Environment variable management
- Health checks
- Auto-scaling configs"""

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        context = task.get("context", {})

        prompt = f"""
Create deployment infrastructure for:

Project: {context.get('project_type', 'application')}
Stack: {context.get('tech_stack', {})}

Generate:
1. Dockerfile (multi-stage)
2. docker-compose.yml
3. GitHub Actions CI/CD
4. Environment configs
5. Deployment documentation
"""

        response = await self.llm.generate(prompt, self.system_prompt)
        return self._parse_response(response, "devops")
