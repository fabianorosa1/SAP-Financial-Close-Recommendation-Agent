"""
Agent configuration store for the Financial Closing Advisor.
Stores and retrieves closing configuration: calendar, ownership,
escalation thresholds, and deadline proximity alert settings.
"""
from datetime import datetime, timezone
from typing import Any, Optional

_config: dict = {
    "closing_calendar": [
        {
            "entity_id": "1000",
            "entity_name": "Company Code 1000",
            "period": f"{datetime.now(timezone.utc).year}-{datetime.now(timezone.utc).month:02d}",
            "closing_date": f"{datetime.now(timezone.utc).year}-{datetime.now(timezone.utc).month:02d}-31T23:59:00Z",
        }
    ],
    "task_ownership": {
        "T001": {"owner_email": "alice.chen@company.com", "owner_name": "Alice Chen"},
        "T002": {"owner_email": "bob.kumar@company.com", "owner_name": "Bob Kumar"},
        "T003": {"owner_email": "carol.smith@company.com", "owner_name": "Carol Smith"},
        "T004": {"owner_email": "david.lee@company.com", "owner_name": "David Lee"},
        "T005": {"owner_email": "emma.wilson@company.com", "owner_name": "Emma Wilson"},
        "T006": {"owner_email": "frank.muller@company.com", "owner_name": "Frank Müller"},
        "T007": {"owner_email": "grace.tanaka@company.com", "owner_name": "Grace Tanaka"},
        "T008": {"owner_email": "henry.brown@company.com", "owner_name": "Henry Brown"},
        "T009": {"owner_email": "irene.patel@company.com", "owner_name": "Irene Patel"},
        "T010": {"owner_email": "james.obrien@company.com", "owner_name": "James O'Brien"},
        "T011": {"owner_email": "karen.liu@company.com", "owner_name": "Karen Liu"},
        "T012": {"owner_email": "alice.chen@company.com", "owner_name": "Alice Chen"},
    },
    "escalation_thresholds": {
        "warning_hours": 8,
        "critical_hours": 4,
        "breach_hours": 0,
    },
    "deadline_proximity_alert_hours": 6,
}


def get_config(section: Optional[str] = None) -> dict:
    """
    Returns the full configuration dict, or a specific section if provided.
    """
    if section:
        return _config.get(section, {})
    return dict(_config)


def update_config(section: str, key: str, value: Any) -> str:
    """
    Updates a specific configuration parameter.
    Returns a confirmation message.
    """
    if section not in _config:
        return f"Configuration section '{section}' not found. Available sections: {list(_config.keys())}"

    if isinstance(_config[section], dict):
        _config[section][key] = value
        return f"Configuration updated: {section}.{key} = {value}"
    else:
        return f"Section '{section}' is not a key-value store and cannot be updated this way."
