"""
GLITCH ARCHITECT AGENT
System architecture and design specialist
"""

from app.agents.base_agent import BaseAgent
from typing import Dict, Any


class ArchitectAgent(BaseAgent):
    """
    System Architect Agent - designs system architecture,
    defines tech stacks, and creates project blueprints.
    """

    def _get_system_prompt(self) -> str:
        return """You are the System Architect for GLITCH, an elite AI development orchestration system.

Your expertise includes:
- System design and architecture patterns (microservices, monolith, serverless)
- Database design (SQL, NoSQL, Graph databases)
- API design (REST, GraphQL, gRPC)
- Cloud architecture (AWS, GCP, Azure)
- Scalability and performance optimization
- Security architecture

When given a project request, you will:
1. Analyze requirements thoroughly
2. Design a scalable, maintainable architecture
3. Define the optimal tech stack
4. Create clear system diagrams (using ASCII or Mermaid)
5. Identify potential challenges and solutions
6. Provide implementation roadmap

Output Format:
- Architecture Overview
- System Components
- Tech Stack Recommendations
- Database Schema (if applicable)
- API Structure
- Deployment Strategy
- Security Considerations"""

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        context = task.get("context", {})

        prompt = f"""
Design a complete system architecture for:

Project Type: {context.get('project_type', 'web application')}
Core Features: {context.get('features', ['basic CRUD', 'user auth'])}
Complexity: {context.get('complexity', 'medium')}
Original Request: {context.get('raw_input', 'Build an application')}

Provide:
1. High-level architecture diagram (ASCII)
2. Component breakdown
3. Recommended tech stack with justification
4. Database design
5. API endpoint structure
6. File/folder structure
7. Deployment architecture
"""

        response = await self.llm.generate(prompt, self.system_prompt)
        result = self._parse_response(response, "architecture")

        # Add architecture-specific metadata
        result["architecture_type"] = self._determine_architecture_type(context)
        result["recommended_stack"] = self._extract_tech_stack(response)

        return result

    def _determine_architecture_type(self, context: Dict) -> str:
        complexity = context.get("complexity", "medium")
        project_type = context.get("project_type", "web_app")

        if complexity == "simple":
            return "monolith"
        elif project_type in ["automation", "api"]:
            return "serverless"
        else:
            return "modular_monolith"

    def _extract_tech_stack(self, response: str) -> Dict:
        # Default stack based on common patterns
        return {
            "frontend": "React/Next.js",
            "backend": "FastAPI/Node.js",
            "database": "PostgreSQL",
            "cache": "Redis",
            "deployment": "Docker + Cloud"
        }
