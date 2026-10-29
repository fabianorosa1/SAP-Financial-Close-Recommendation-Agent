"""
Tool: get_task_dependencies
Returns the dependency map for the current closing plan.
"""
from langchain_core.tools import StructuredTool
from pydantic import BaseModel
from closing_task_store import get_closing_tasks


class GetTaskDependenciesInput(BaseModel):
    pass


def get_task_dependencies() -> dict:
    """Return the dependency map for the current closing plan."""
    tasks = get_closing_tasks()
    dependency_map = {}
    for task in tasks:
        dependency_map[task["task_id"]] = {
            "description": task["description"],
            "depends_on": task["dependencies"],
            "status": task["status"],
        }
    return {
        "dependency_map": dependency_map,
        "total_tasks": len(dependency_map),
    }


get_task_dependencies_tool = StructuredTool.from_function(
    func=get_task_dependencies,
    name="get_task_dependencies",
    description="Return the dependency map for the current closing plan. Shows which tasks must be completed before others can start.",
    args_schema=GetTaskDependenciesInput,
)
