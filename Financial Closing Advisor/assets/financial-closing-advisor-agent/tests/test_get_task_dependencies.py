"""Unit tests for get_task_dependencies tool."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from tools.get_task_dependencies import get_task_dependencies


def test_get_task_dependencies_returns_map():
    result = get_task_dependencies()
    assert "dependency_map" in result
    assert "total_tasks" in result
    assert result["total_tasks"] > 0


def test_dependency_map_has_required_fields():
    result = get_task_dependencies()
    for task_id, info in result["dependency_map"].items():
        assert "description" in info
        assert "depends_on" in info
        assert "status" in info
        assert isinstance(info["depends_on"], list)


def test_dependencies_reference_valid_task_ids():
    result = get_task_dependencies()
    all_task_ids = set(result["dependency_map"].keys())
    for task_id, info in result["dependency_map"].items():
        for dep in info["depends_on"]:
            assert dep in all_task_ids, f"Task {task_id} depends on {dep} which does not exist"


def test_some_tasks_have_no_dependencies():
    result = get_task_dependencies()
    root_tasks = [tid for tid, info in result["dependency_map"].items() if not info["depends_on"]]
    assert len(root_tasks) > 0, "There should be at least one root task with no dependencies"


def test_some_tasks_have_dependencies():
    result = get_task_dependencies()
    dependent_tasks = [tid for tid, info in result["dependency_map"].items() if info["depends_on"]]
    assert len(dependent_tasks) > 0, "There should be at least one task with dependencies"
