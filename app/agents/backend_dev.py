"""
GLITCH BACKEND DEVELOPER AGENT
Server-side development specialist
"""

from app.agents.base_agent import BaseAgent
from typing import Dict, Any


class BackendDevAgent(BaseAgent):
    """
    Backend Developer Agent - API development,
    database design, server architecture.
    """

    def _get_system_prompt(self) -> str:
        return """You are a Senior Backend Developer for GLITCH.

Your expertise includes:
- API Development: REST, GraphQL, gRPC
- Languages: Python, Node.js, Go, Rust
- Frameworks: FastAPI, Django, Express, NestJS
- Databases: PostgreSQL, MySQL, MongoDB, Redis
- ORMs: SQLAlchemy, Prisma, TypeORM
- Authentication: JWT, OAuth2, API Keys
- Queues: Celery, Bull, RabbitMQ
- Caching: Redis, Memcached

You build:
1. Scalable API endpoints
2. Database schemas and migrations
3. Authentication systems
4. Background job processors
5. Caching layers
6. Data validation

Always output production-ready code with:
- Proper error handling
- Input validation
- Security best practices
- Clear documentation"""

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        context = task.get("context", {})

        prompt = f"""
Build backend implementation for:

Project: {context.get('project_type', 'application')}
Features: {context.get('features', [])}
Tech Stack: {context.get('tech_stack', {})}

Generate:
1. API routes and controllers
2. Database models/schemas
3. Service layer logic
4. Middleware (auth, validation)
5. Configuration files
"""

        response = await self.llm.generate(prompt, self.system_prompt)
        return self._parse_response(response, "backend")
