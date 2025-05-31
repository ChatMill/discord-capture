import pytest
from interfaces.schemas import payload_schema
from domain.entities.task import Task

class DummyInteraction:
    def __init__(self):
        self.guild_id = 1
        self.channel_id = 2
        self.id = 3
        self.user = type("User", (), {"id": 4})()

def test_build_task_payload():
    interaction = DummyInteraction()
    message_ids = [123, 456]
    task = payload_schema.build_task_payload(interaction, message_ids)
    assert isinstance(task, Task)
    assert task.chatmill_id == "missspec-1-2-3"
    assert task.message_ids == ["123", "456"]
    assert task.assignees == ["4"]
    assert task.title == "需求草案标题示例"
    assert task.description == "需求描述示例，后续可自动生成或由用户补充" 