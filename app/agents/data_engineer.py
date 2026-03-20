"""
GLITCH DATA ENGINEER AGENT
Data pipelines and analytics specialist
"""

from app.agents.base_agent import BaseAgent
from typing import Dict, Any


class DataEngineerAgent(BaseAgent):
    """
    Data Engineer Agent - builds data pipelines,
    analytics, and data infrastructure.
    """

    def _get_system_prompt(self) -> str:
        return """You are a Senior Data Engineer for GLITCH.

Your expertise includes:
- Databases: PostgreSQL, MongoDB, ClickHouse
- Data Pipelines: Apache Airflow, Prefect, Dagster
- ETL: dbt, Fivetran, custom scripts
- Streaming: Kafka, Redis Streams
- Analytics: Metabase, Grafana, custom
- Data Lakes: S3, Parquet, Delta Lake
- Vector DBs: Pinecone, Weaviate, Chroma
- Search: Elasticsearch, Meilisearch

You build:
1. Database schemas and migrations
2. ETL pipelines
3. Data warehouses
4. Analytics dashboards
5. Real-time streaming
6. Vector stores for AI
7. Search indices

Data principles:
- Data quality first
- Scalable architectures
- Clear documentation
- Performance optimization"""

    async def _process_task(self, task: Dict) -> Dict[str, Any]:
        context = task.get("context", {})

        prompt = f"""
Build data infrastructure for:

Project: {context.get('project_type', 'application')}
Features: {context.get('features', [])}

Generate:
1. Database schema design
2. Migration scripts
3. ETL pipeline code
4. Analytics queries
5. Data models
"""

        response = await self.llm.generate(prompt, self.system_prompt)
        return self._parse_response(response, "data")
