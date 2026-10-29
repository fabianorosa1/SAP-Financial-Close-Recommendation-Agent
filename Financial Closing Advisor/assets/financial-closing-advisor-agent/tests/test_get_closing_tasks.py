"""Unit tests for get_closing_tasks tool."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from tools.get_closing_tasks import get_closing_tasks


def test_get_closing_tasks_returns_tasks():
    result = get_closing_tasks()
    assert "tasks" in result
    assert "period" in result
    assert "total_tasks" in result
    assert result["total_tasks"] == len(result["tasks"])


def test_get_closing_tasks_has_required_fields():
    result = get_closing_tasks()
    for task in result["tasks"]:
        assert "task_id" in task
        assert "description" in task
        assert "status" in task
        assert "owner" in task
        assert "priority" in task
        assert "deadline" in task
        assert "dependencies" in task


def test_get_closing_tasks_has_blocked_task():
    result = get_closing_tasks()
    statuses = [t["status"] for t in result["tasks"]]
    assert "blocked" in statuses


def test_get_closing_tasks_has_in_progress_task():
    result = get_closing_tasks()
    statuses = [t["status"] for t in result["tasks"]]
    assert "in-progress" in statuses


def test_get_closing_tasks_has_completed_task():
    result = get_closing_tasks()
    statuses = [t["status"] for t in result["tasks"]]
    assert "completed" in statuses


def test_get_closing_tasks_with_period():
    result = get_closing_tasks(period="2024-12")
    assert result["period"] == "2024-12"
    assert len(result["tasks"]) > 0


def test_get_closing_tasks_blocked_has_error_or_missing_fields():
    result = get_closing_tasks()
    blocked = [t for t in result["tasks"] if t["status"] == "blocked"]
    assert len(blocked) >= 2
    for task in blocked:
        has_error = bool(task.get("error_message"))
        has_missing = bool(task.get("missing_fields"))
        assert has_error or has_missing, f"Blocked task {task['task_id']} has no error or missing fields"
