"""
GLITCH MEMORY SERVICE
Persistent memory and context management
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import os


class MemoryService:
    """
    Service for managing GLITCH's memory system.
    Stores projects, builds, decisions, and context.
    """

    def __init__(self, storage_path: str = "./data"):
        self.storage_path = storage_path
        self.projects: Dict[str, Dict] = {}
        self.conversations: Dict[str, List] = {}
        self.decisions: List[Dict] = []
        self._ensure_storage()
        self._load_memory()

    def _ensure_storage(self):
        """Ensure storage directory exists."""
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(f"{self.storage_path}/projects", exist_ok=True)
        os.makedirs(f"{self.storage_path}/conversations", exist_ok=True)

    def _load_memory(self):
        """Load memory from storage."""
        # Load projects
        projects_file = f"{self.storage_path}/projects.json"
        if os.path.exists(projects_file):
            with open(projects_file, 'r') as f:
                self.projects = json.load(f)

        # Load decisions
        decisions_file = f"{self.storage_path}/decisions.json"
        if os.path.exists(decisions_file):
            with open(decisions_file, 'r') as f:
                self.decisions = json.load(f)

    def _save_memory(self):
        """Save memory to storage."""
        with open(f"{self.storage_path}/projects.json", 'w') as f:
            json.dump(self.projects, f, indent=2, default=str)

        with open(f"{self.storage_path}/decisions.json", 'w') as f:
            json.dump(self.decisions, f, indent=2, default=str)

    # Project Memory
    def create_project(self, project_id: str, data: Dict) -> Dict:
        """Create a new project in memory."""
        project = {
            "id": project_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "active",
            **data
        }
        self.projects[project_id] = project
        self._save_memory()
        return project

    def get_project(self, project_id: str) -> Optional[Dict]:
        """Get a project by ID."""
        return self.projects.get(project_id)

    def update_project(self, project_id: str, updates: Dict) -> Optional[Dict]:
        """Update a project."""
        if project_id in self.projects:
            self.projects[project_id].update(updates)
            self.projects[project_id]["updated_at"] = datetime.now().isoformat()
            self._save_memory()
            return self.projects[project_id]
        return None

    def list_projects(self) -> List[Dict]:
        """List all projects."""
        return list(self.projects.values())

    def delete_project(self, project_id: str) -> bool:
        """Delete a project."""
        if project_id in self.projects:
            del self.projects[project_id]
            self._save_memory()
            return True
        return False

    # Conversation Memory
    def add_message(self, conversation_id: str, role: str, content: str):
        """Add a message to a conversation."""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        self.conversations[conversation_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

        # Save conversation
        conv_file = f"{self.storage_path}/conversations/{conversation_id}.json"
        with open(conv_file, 'w') as f:
            json.dump(self.conversations[conversation_id], f, indent=2)

    def get_conversation(self, conversation_id: str) -> List[Dict]:
        """Get a conversation history."""
        if conversation_id in self.conversations:
            return self.conversations[conversation_id]

        # Try loading from file
        conv_file = f"{self.storage_path}/conversations/{conversation_id}.json"
        if os.path.exists(conv_file):
            with open(conv_file, 'r') as f:
                self.conversations[conversation_id] = json.load(f)
                return self.conversations[conversation_id]

        return []

    def get_context(self, conversation_id: str, max_messages: int = 10) -> str:
        """Get conversation context as a string."""
        messages = self.get_conversation(conversation_id)[-max_messages:]
        return "\n".join([
            f"{m['role']}: {m['content']}"
            for m in messages
        ])

    # Decision Memory
    def record_decision(
        self,
        project_id: str,
        decision_type: str,
        decision: str,
        reasoning: str
    ):
        """Record an architectural or technical decision."""
        self.decisions.append({
            "project_id": project_id,
            "type": decision_type,
            "decision": decision,
            "reasoning": reasoning,
            "timestamp": datetime.now().isoformat()
        })
        self._save_memory()

    def get_project_decisions(self, project_id: str) -> List[Dict]:
        """Get all decisions for a project."""
        return [d for d in self.decisions if d["project_id"] == project_id]

    # Search and Retrieval
    def search_projects(self, query: str) -> List[Dict]:
        """Search projects by query."""
        results = []
        query_lower = query.lower()

        for project in self.projects.values():
            # Search in project name and description
            if (query_lower in project.get("name", "").lower() or
                query_lower in project.get("description", "").lower() or
                query_lower in str(project.get("features", [])).lower()):
                results.append(project)

        return results

    def get_similar_projects(self, project_type: str) -> List[Dict]:
        """Get similar projects by type."""
        return [
            p for p in self.projects.values()
            if p.get("project_type") == project_type
        ]
