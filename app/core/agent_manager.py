"""
GLITCH AGENT MANAGER
Spawns, tracks, and manages AI agent lifecycle
"""

from typing import Dict, List, Optional
from datetime import datetime
import asyncio


class BaseAgent:
    """Base class for all GLITCH agents."""

    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.status = "idle"
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        self.current_task = None
        self.completed_tasks = []

    async def execute(self, task: Dict) -> Dict:
        """Execute a task - override in subclasses."""
        raise NotImplementedError

    def update_status(self, status: str):
        self.status = status
        self.last_active = datetime.now()


class AgentManager:
    """
    Manages the lifecycle of all GLITCH agents.
    - Spawns new agents
    - Tracks active agents
    - Kills idle agents
    - Routes tasks to appropriate agents
    """

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_pool: Dict[str, List[BaseAgent]] = {}
        self.max_agents_per_type = 5
        self.idle_timeout = 300  # 5 minutes

    async def get_agent(self, agent_type: str) -> BaseAgent:
        """
        Get an available agent of the specified type, or spawn a new one.
        """
        # Check for available agent in pool
        if agent_type in self.agent_pool:
            for agent in self.agent_pool[agent_type]:
                if agent.status == "idle":
                    agent.update_status("assigned")
                    return agent

        # Spawn new agent if pool isn't full
        if agent_type not in self.agent_pool:
            self.agent_pool[agent_type] = []

        if len(self.agent_pool[agent_type]) < self.max_agents_per_type:
            agent = await self.spawn_agent(agent_type)
            return agent

        # Wait for an agent to become available
        return await self.wait_for_agent(agent_type)

    async def spawn_agent(self, agent_type: str) -> BaseAgent:
        """
        Spawn a new agent of the specified type.
        """
        from app.agents.ai_engineer import AIEngineerAgent
        from app.agents.fullstack_dev import FullstackDevAgent
        from app.agents.backend_dev import BackendDevAgent
        from app.agents.frontend_dev import FrontendDevAgent
        from app.agents.devops import DevOpsAgent
        from app.agents.uiux import UIUXAgent
        from app.agents.architect import ArchitectAgent
        from app.agents.mobile_dev import MobileDevAgent
        from app.agents.qa_engineer import QAEngineerAgent
        from app.agents.security_engineer import SecurityEngineerAgent
        from app.agents.data_engineer import DataEngineerAgent
        from app.agents.tech_lead import TechLeadAgent
        from app.agents.product_manager import ProductManagerAgent

        agent_classes = {
            "architect": ArchitectAgent,
            "ai_engineer": AIEngineerAgent,
            "fullstack_dev": FullstackDevAgent,
            "backend_dev": BackendDevAgent,
            "frontend_dev": FrontendDevAgent,
            "mobile_dev": MobileDevAgent,
            "devops": DevOpsAgent,
            "uiux": UIUXAgent,
            "qa_engineer": QAEngineerAgent,
            "security_engineer": SecurityEngineerAgent,
            "data_engineer": DataEngineerAgent,
            "tech_lead": TechLeadAgent,
            "product_manager": ProductManagerAgent,
        }

        agent_class = agent_classes.get(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")

        agent_id = f"{agent_type}_{len(self.agent_pool.get(agent_type, [])) + 1}"
        agent = agent_class(agent_id, agent_type)

        if agent_type not in self.agent_pool:
            self.agent_pool[agent_type] = []

        self.agent_pool[agent_type].append(agent)
        self.agents[agent_id] = agent

        return agent

    async def wait_for_agent(self, agent_type: str, timeout: int = 60) -> BaseAgent:
        """
        Wait for an agent to become available.
        """
        start_time = datetime.now()

        while (datetime.now() - start_time).seconds < timeout:
            for agent in self.agent_pool.get(agent_type, []):
                if agent.status == "idle":
                    agent.update_status("assigned")
                    return agent
            await asyncio.sleep(1)

        raise TimeoutError(f"No {agent_type} agent available after {timeout}s")

    def release_agent(self, agent_id: str):
        """
        Release an agent back to the pool.
        """
        if agent_id in self.agents:
            self.agents[agent_id].update_status("idle")

    async def kill_agent(self, agent_id: str):
        """
        Kill and remove an agent.
        """
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent_type = agent.agent_type

            # Remove from pool
            if agent_type in self.agent_pool:
                self.agent_pool[agent_type] = [
                    a for a in self.agent_pool[agent_type] if a.agent_id != agent_id
                ]

            # Remove from agents dict
            del self.agents[agent_id]

    async def kill_idle_agents(self):
        """
        Kill all agents that have been idle for too long.
        """
        now = datetime.now()
        to_kill = []

        for agent_id, agent in self.agents.items():
            if agent.status == "idle":
                idle_time = (now - agent.last_active).seconds
                if idle_time > self.idle_timeout:
                    to_kill.append(agent_id)

        for agent_id in to_kill:
            await self.kill_agent(agent_id)

        return len(to_kill)

    async def kill_project_agents(self, project_id: str):
        """
        Kill all agents working on a specific project.
        """
        to_kill = []
        for agent_id, agent in self.agents.items():
            if agent.current_task and agent.current_task.get("project_id") == project_id:
                to_kill.append(agent_id)

        for agent_id in to_kill:
            await self.kill_agent(agent_id)

    def get_status(self) -> Dict:
        """
        Get current status of all agents.
        """
        status = {
            "total_agents": len(self.agents),
            "by_type": {},
            "by_status": {"idle": 0, "assigned": 0, "working": 0}
        }

        for agent_type, agents in self.agent_pool.items():
            status["by_type"][agent_type] = {
                "count": len(agents),
                "idle": len([a for a in agents if a.status == "idle"]),
                "working": len([a for a in agents if a.status == "working"])
            }

        for agent in self.agents.values():
            if agent.status in status["by_status"]:
                status["by_status"][agent.status] += 1

        return status
