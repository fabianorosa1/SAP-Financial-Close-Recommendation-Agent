"""
Tool: get_period_status
Returns the open/closed status of the current financial period.
"""
from datetime import datetime, timezone, timedelta
from langchain_core.tools import StructuredTool
from pydantic import BaseModel


class GetPeriodStatusInput(BaseModel):
    pass


def get_period_status() -> dict:
    """Return the open/closed status and closing deadline of the current financial period."""
    now = datetime.now(timezone.utc)
    period = f"{now.year}-{now.month:02d}"
    closing_deadline = (now + timedelta(days=1)).replace(hour=23, minute=59, second=0, microsecond=0)
    return {
        "period": period,
        "status": "open",
        "closing_deadline": closing_deadline.isoformat(),
        "company_code": "1000",
        "ledger": "0L",
    }


get_period_status_tool = StructuredTool.from_function(
    func=get_period_status,
    name="get_period_status",
    description="Return the open/closed status and closing deadline of the current financial period.",
    args_schema=GetPeriodStatusInput,
)
