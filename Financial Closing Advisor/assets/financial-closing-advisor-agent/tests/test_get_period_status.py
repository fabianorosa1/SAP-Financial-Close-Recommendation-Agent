"""Unit tests for get_period_status tool."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from tools.get_period_status import get_period_status


def test_get_period_status_returns_required_fields():
    result = get_period_status()
    assert "period" in result
    assert "status" in result
    assert "closing_deadline" in result


def test_period_status_is_open_or_closed():
    result = get_period_status()
    assert result["status"] in ("open", "closed")


def test_period_format():
    result = get_period_status()
    # Period should be YYYY-MM format
    parts = result["period"].split("-")
    assert len(parts) == 2
    assert len(parts[0]) == 4  # Year
    assert len(parts[1]) == 2  # Month


def test_closing_deadline_is_iso_string():
    result = get_period_status()
    from datetime import datetime
    # Should parse without error
    deadline_str = result["closing_deadline"]
    assert isinstance(deadline_str, str)
    assert len(deadline_str) > 10
