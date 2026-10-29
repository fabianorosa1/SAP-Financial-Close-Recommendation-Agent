"""
Tool: get_closing_config
Reads the closing configuration from the agent config store.
"""
from typing import Optional
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from closing_config_store import get_config


class GetClosingConfigInput(BaseModel):
    section: Optional[str] = Field(
        default=None,
        description="Configuration section to retrieve (e.g. 'closing_calendar', 'task_ownership', 'escalation_thresholds', 'deadline_proximity_alert_hours'). Omit for full config."
    )


def get_closing_config(section: Optional[str] = None) -> dict:
    """Read the closing configuration from the agent config store."""
    result = get_config(section=section)
    if section:
        return {"section": section, "config": result}
    return {"config": result}


get_closing_config_tool = StructuredTool.from_function(
    func=get_closing_config,
    name="get_closing_config",
    description="Read the closing calendar, task ownership, escalation thresholds, and deadline proximity configuration. Optionally filter by section.",
    args_schema=GetClosingConfigInput,
)
