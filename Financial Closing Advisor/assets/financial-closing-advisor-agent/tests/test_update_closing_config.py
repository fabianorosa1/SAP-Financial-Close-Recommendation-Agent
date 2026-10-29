"""Unit tests for update_closing_config tool."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from tools.update_closing_config import update_closing_config
from tools.get_closing_config import get_closing_config


def test_update_escalation_threshold():
    result = update_closing_config(section="escalation_thresholds", key="warning_hours", value=10)
    assert "updated" in result.lower() or "configuration" in result.lower()


def test_updated_value_is_reflected_in_get_config():
    update_closing_config(section="escalation_thresholds", key="warning_hours", value=7)
    config_result = get_closing_config(section="escalation_thresholds")
    assert config_result["config"]["warning_hours"] == 7
    # Restore original value
    update_closing_config(section="escalation_thresholds", key="warning_hours", value=8)


def test_update_deadline_proximity():
    update_closing_config(section="escalation_thresholds", key="critical_hours", value=5)
    config_result = get_closing_config(section="escalation_thresholds")
    assert config_result["config"]["critical_hours"] == 5
    # Restore
    update_closing_config(section="escalation_thresholds", key="critical_hours", value=4)


def test_update_invalid_section_returns_error():
    result = update_closing_config(section="nonexistent_section", key="some_key", value="some_value")
    assert "not found" in result.lower() or "error" in result.lower() or "available" in result.lower()
