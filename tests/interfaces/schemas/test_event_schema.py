import pytest
from interfaces.schemas import event_schema
from domain.entities.message import Message
from domain.entities.task import Task
from domain.value_objects.agent_profile import AgentProfile

class DummyInteraction:
    def __init__(self):
        self.guild_id = 1
        self.channel_id = 2
        self.id = 3
        self.user = type("User", (), {"id": 4})()
        self.client = type("Client", (), {"avatar_url": "avatar"})()

def test_build_capture_event(monkeypatch):
    # 用真实 Interaction、Message、Task
    interaction = DummyInteraction()
    messages = [Message(id="m1", author_id="a1", author_name="n1", content="c1", timestamp="t1"),
                Message(id="m2", author_id="a2", author_name="n2", content="c2", timestamp="t2")]
    task = Task(chatmill_id="cmid", message_ids=["m1", "m2"], title="t", description="d")
    session_id = "sid"
    # Patch WebhookName.MISSSPEC.value
    monkeypatch.setattr(event_schema, "WebhookName", type("WebhookName", (), {"MISSSPEC": type("MISSSPEC", (), {"value": "wh"})()})())
    event = event_schema.build_capture_event(interaction, messages, task, session_id)
    # 检查字段
    assert event.session_id == session_id
    assert event.event_id.startswith("evt-1-2-3")
    assert event.operator_id == "4"
    assert event.payload == task
    assert event.messages == messages
    assert event.agent_profile.webhook_name == "wh"
    assert event.agent_profile.channel_id == 2
    assert event.agent_profile.guild_id == 1
    assert event.agent_profile.avatar_url == "avatar"
    assert event.history == [] 