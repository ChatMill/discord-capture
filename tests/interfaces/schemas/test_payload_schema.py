import pytest
from interfaces.schemas import payload_schema
from domain.entities.spec import Spec

class DummyInteraction:
    def __init__(self):
        self.guild_id = 1
        self.channel_id = 2
        self.id = 3
        self.user = type("User", (), {"id": 4})()

def test_build_spec_payload():
    interaction = DummyInteraction()
    message_ids = [123, 456]
    spec = payload_schema.build_spec_payload(interaction, message_ids)
    assert isinstance(spec, Spec)
    assert spec.chatmill_id == "missspec-1-2-3"
    assert spec.message_ids == ["123", "456"]
    assert spec.assignees == ["4"]
    assert spec.title == "需求草案标题示例"
    assert spec.description == "需求描述示例，后续可自动生成或由用户补充"