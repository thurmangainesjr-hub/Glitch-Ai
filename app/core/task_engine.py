"""
GLITCH TASK ENGINE
Queue system for parallel task execution and progress tracking
"""

from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
import asyncio
import uuid


class TaskStatus(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task:
    """Represents a single task in the GLITCH system."""

    def __init__(self, task_data: Dict):
        self.id = task_data.get("id", str(uuid.uuid4()))
        self.phase = task_data.get("phase", "unknown")
        self.type = task_data.get("type", "development")
        self.agent = task_data.get("agent", "fullstack_dev")
        self.context = task_data.get("context", {})
        self.status = TaskStatus(task_data.get("status", "pending"))
        self.dependencies = task_data.get("dependencies", [])
        self.priority = task_data.get("priority", 5)
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None
        self.progress = 0

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "phase": self.phase,
            "type": self.type,
            "agent": self.agent,
            "status": self.status.value,
            "priority": self.priority,
            "progress": self.progress,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class TaskEngine:
    """
    Manages task queuing, execution, and tracking.
    - Maintains task queue
    - Handles parallel execution
    - Tracks progress
    - Manages dependencies
    """

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.queue: List[str] = []  # Task IDs in priority order
        self.completed: List[str] = []
        self.failed: List[str] = []
        self.max_parallel = 3

    def add_task(self, task_data: Dict) -> str:
        """
        Add a new task to the engine.
        """
        task = Task(task_data)
        self.tasks[task.id] = task

        # Insert into queue based on priority
        inserted = False
        for i, task_id in enumerate(self.queue):
            if self.tasks[task_id].priority > task.priority:
                self.queue.insert(i, task.id)
                inserted = True
                break

        if not inserted:
            self.queue.append(task.id)

        return task.id

    def update_status(self, task_id: str, status: str):
        """
        Update the status of a task.
        """
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        task.status = TaskStatus(status)

        if status == "in_progress":
            task.started_at = datetime.now()
            if task_id in self.queue:
                self.queue.remove(task_id)

        elif status == "completed":
            task.completed_at = datetime.now()
            task.progress = 100
            self.completed.append(task_id)

        elif status == "failed":
            task.completed_at = datetime.now()
            self.failed.append(task_id)

        return True

    def update_progress(self, task_id: str, progress: int):
        """
        Update task progress (0-100).
        """
        if task_id in self.tasks:
            self.tasks[task_id].progress = min(100, max(0, progress))
            return True
        return False

    def set_result(self, task_id: str, result: Dict):
        """
        Set the result of a completed task.
        """
        if task_id in self.tasks:
            self.tasks[task_id].result = result
            return True
        return False

    def set_error(self, task_id: str, error: str):
        """
        Set error for a failed task.
        """
        if task_id in self.tasks:
            self.tasks[task_id].error = error
            return True
        return False

    def get_next_tasks(self, count: int = 1) -> List[Task]:
        """
        Get the next tasks to execute (respecting dependencies).
        """
        ready_tasks = []

        for task_id in self.queue:
            task = self.tasks[task_id]

            # Check if all dependencies are completed
            deps_met = all(
                dep_id in self.completed
                for dep_id in task.dependencies
            )

            if deps_met:
                ready_tasks.append(task)
                if len(ready_tasks) >= count:
                    break

        return ready_tasks

    def can_execute_parallel(self) -> int:
        """
        Get number of tasks that can be executed in parallel.
        """
        in_progress = len([
            t for t in self.tasks.values()
            if t.status == TaskStatus.IN_PROGRESS
        ])
        return max(0, self.max_parallel - in_progress)

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a specific task by ID.
        """
        return self.tasks.get(task_id)

    def get_project_progress(self) -> Dict:
        """
        Get overall project progress.
        """
        total = len(self.tasks)
        if total == 0:
            return {"progress": 0, "status": "no_tasks"}

        completed_count = len(self.completed)
        failed_count = len(self.failed)
        in_progress = len([
            t for t in self.tasks.values()
            if t.status == TaskStatus.IN_PROGRESS
        ])

        # Calculate weighted progress
        total_progress = sum(t.progress for t in self.tasks.values())
        avg_progress = total_progress / total

        return {
            "progress": round(avg_progress, 1),
            "total_tasks": total,
            "completed": completed_count,
            "in_progress": in_progress,
            "pending": len(self.queue),
            "failed": failed_count,
            "status": self._determine_status()
        }

    def _determine_status(self) -> str:
        """
        Determine overall project status.
        """
        if len(self.failed) > 0:
            return "has_failures"
        if len(self.completed) == len(self.tasks):
            return "completed"
        if any(t.status == TaskStatus.IN_PROGRESS for t in self.tasks.values()):
            return "in_progress"
        if len(self.queue) > 0:
            return "pending"
        return "unknown"

    def get_all_tasks(self) -> List[Dict]:
        """
        Get all tasks as dictionaries.
        """
        return [task.to_dict() for task in self.tasks.values()]

    def clear(self):
        """
        Clear all tasks.
        """
        self.tasks.clear()
        self.queue.clear()
        self.completed.clear()
        self.failed.clear()
