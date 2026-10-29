"""
Tool: get_closing_tasks
Returns all closing tasks for the active (or specified) financial period.
"""
from typing import Optional
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from closing_task_store import get_closing_tasks as _get_tasks, get_active_period


class GetClosingTasksInput(BaseModel):
    period: Optional[str] = Field(
        default=None,
        description="Financial period to retrieve tasks for (e.g. '2024-12'). Defaults to the active period."
    )


def get_closing_tasks(period: Optional[str] = None) -> dict:
    """Retrieve all closing tasks for the active (or specified) financial period."""
    active_period = period or get_active_period()
    tasks = _get_tasks(period=active_period)
    return {
        "period": active_period,
        "total_tasks": len(tasks),
        "tasks": tasks,
    }


get_closing_tasks_tool = StructuredTool.from_function(
    func=get_closing_tasks,
    name="get_closing_tasks",
    description="Retrieve all closing tasks for the active (or specified) financial period. Returns task status, owner, priority, deadline, dependencies, and any error messages.",
    args_schema=GetClosingTasksInput,
)
