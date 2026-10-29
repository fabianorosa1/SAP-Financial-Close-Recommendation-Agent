"""
Tool: update_closing_config
Updates a specific configuration parameter in the agent config store.
"""
from typing import Any
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from closing_config_store import update_config


class UpdateClosingConfigInput(BaseModel):
    section: str = Field(
        description="Configuration section to update (e.g. 'escalation_thresholds', 'deadline_proximity_alert_hours')."
    )
    key: str = Field(
        description="The specific configuration key to update within the section (e.g. 'warning_hours', 'critical_hours')."
    )
    value: Any = Field(
        description="The new value to set for the configuration key."
    )


def update_closing_config(section: str, key: str, value: Any) -> str:
    """Update a specific configuration parameter. Requires explicit controller confirmation before executing."""
    return update_config(section=section, key=key, value=value)


update_closing_config_tool = StructuredTool.from_function(
    func=update_closing_config,
    name="update_closing_config",
    description="Update a specific configuration parameter (e.g. escalation thresholds, deadline proximity alert hours, task ownership). Always confirm with the user before calling this tool.",
    args_schema=UpdateClosingConfigInput,
)
