"""Unit tests for get_closing_config tool."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from tools.get_closing_config import get_closing_config


def test_get_closing_config_full_returns_all_sections():
    result = get_closing_config()
    config = result["config"]
    assert "closing_calendar" in config
    assert "task_ownership" in config
    assert "escalation_thresholds" in config
    assert "deadline_proximity_alert_hours" in config


def test_get_closing_config_section_escalation():
    result = get_closing_config(section="escalation_thresholds")
    assert result["section"] == "escalation_thresholds"
    config = result["config"]
    assert "warning_hours" in config
    assert "critical_hours" in config
    assert "breach_hours" in config


def test_get_closing_config_section_deadline_proximity():
    result = get_closing_config(section="deadline_proximity_alert_hours")
    assert "config" in result
    assert isinstance(result["config"], int)


def test_get_closing_config_task_ownership():
    result = get_closing_config(section="task_ownership")
    config = result["config"]
    assert isinstance(config, dict)
    assert len(config) > 0
    # Each entry should have owner_email and owner_name
    for task_id, owner_info in config.items():
        assert "owner_email" in owner_info
        assert "owner_name" in owner_info


def test_get_closing_config_closing_calendar():
    result = get_closing_config(section="closing_calendar")
    calendar = result["config"]
    assert isinstance(calendar, list)
    assert len(calendar) > 0
    for entry in calendar:
        assert "entity_id" in entry
        assert "period" in entry
