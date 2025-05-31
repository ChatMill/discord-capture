import pytest
import asyncio
from application.services.feedback_utils import agent_response_with_retry

class DummyAgentProfile:
    pass

class DummyAgentResponse:
    def __init__(self, success=True, error=None):
        self.success = success
        self.error = error

@pytest.mark.asyncio
async def test_success_feedback(monkeypatch):
    calls = []
    async def notify(event):
        return DummyAgentResponse(success=True)
    async def send(agent_profile, content):
        calls.append(content)
    await agent_response_with_retry(
        agent_profile=DummyAgentProfile(),
        event=None,
        notify_func=notify,
        send_func=send,
        success_feedback="OK!",
        error_feedback="ERR: {error_msg}",
        retry_feedbacks=["retry1", "retry2", "final"],
        max_retries=3,
        retry_interval=0
    )
    assert calls == ["OK!"]

@pytest.mark.asyncio
async def test_error_feedback(monkeypatch):
    calls = []
    async def notify(event):
        return DummyAgentResponse(success=False, error="fail reason")
    async def send(agent_profile, content):
        calls.append(content)
    await agent_response_with_retry(
        agent_profile=DummyAgentProfile(),
        event=None,
        notify_func=notify,
        send_func=send,
        success_feedback="OK!",
        error_feedback="ERR: {error_msg}",
        retry_feedbacks=["retry1", "retry2", "final"],
        max_retries=3,
        retry_interval=0
    )
    assert calls == ["ERR: fail reason"]

@pytest.mark.asyncio
async def test_retry_and_final(monkeypatch):
    calls = []
    count = {"n": 0}
    async def notify(event):
        count["n"] += 1
        raise Exception("network fail")
    async def send(agent_profile, content):
        calls.append(content)
    await agent_response_with_retry(
        agent_profile=DummyAgentProfile(),
        event=None,
        notify_func=notify,
        send_func=send,
        success_feedback="OK!",
        error_feedback="ERR: {error_msg}",
        retry_feedbacks=["retry1", "retry2", "final {error_type} {error_msg}"],
        max_retries=3,
        retry_interval=0
    )
    # 前两次重试+最后一次兜底
    assert calls[0] == "retry1"
    assert calls[1] == "retry2"
    assert calls[2].startswith("final Exception network fail")
    assert count["n"] == 3 