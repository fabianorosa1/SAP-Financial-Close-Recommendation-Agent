"""Integration test for the Financial Closing Advisor Agent end-to-end flow."""
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

import pytest


@pytest.mark.asyncio
async def test_agent_invoke_closing_status():
    """Test end-to-end agent invoke for a closing status query."""
    from agent import SampleAgent
    from tools.get_closing_tasks import get_closing_tasks_tool
    from tools.get_task_dependencies import get_task_dependencies_tool
    from tools.get_period_status import get_period_status_tool
    from tools.get_closing_config import get_closing_config_tool
    from tools.update_closing_config import update_closing_config_tool

    mock_llm_response = MagicMock()
    mock_llm_response.content = (
        "Here are the current closing task statuses:\n"
        "- T001: Accounts Payable Reconciliation - COMPLETED\n"
        "- T002: Accounts Receivable Clearing - COMPLETED\n"
        "- T003: Fixed Asset Depreciation Run - IN-PROGRESS\n"
        "- T004: Inventory Valuation - BLOCKED (period not open)\n"
        "Total: 12 tasks, 2 completed, 1 in-progress, 3 blocked, 6 pending."
    )

    fake_result = {"messages": [mock_llm_response]}

    tools = [
        get_closing_tasks_tool,
        get_task_dependencies_tool,
        get_period_status_tool,
        get_closing_config_tool,
        update_closing_config_tool,
    ]

    with patch("agent.get_user_sub", return_value="test-user"):
        agent = SampleAgent()
        # Patch the _invoke method to return mocked LLM response
        agent._invoke = AsyncMock(return_value=fake_result)

        result = await agent.invoke(
            query="What are the current closing task statuses?",
            context_id="test-context-001",
            tools=tools,
        )

    assert result.status == "completed"
    assert "task" in result.message.lower() or "status" in result.message.lower() or "completed" in result.message.lower()


@pytest.mark.asyncio
async def test_agent_stream_returns_response():
    """Test that the agent stream yields a completed response."""
    from agent import SampleAgent

    mock_response = MagicMock()
    mock_response.content = "The next recommended action is to run the Accruals Posting (T007)."
    fake_result = {"messages": [mock_response]}

    with patch("agent.get_user_sub", return_value="test-user"):
        agent = SampleAgent()
        agent._invoke = AsyncMock(return_value=fake_result)

        responses = []
        async for chunk in agent.stream(
            query="What should I action next?",
            context_id="test-context-002",
        ):
            responses.append(chunk)

    assert len(responses) >= 2  # At least processing + final
    final = responses[-1]
    assert final["is_task_complete"] is True
    assert "content" in final
