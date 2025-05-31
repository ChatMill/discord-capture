import pytest
from domain.entities.task import Task

class TestTask:
    """
    Unit tests for the Task entity.
    """
    def test_task_creation(self):
        """Test creating a Task entity with all fields."""
        task = Task(
            chatmill_id="cmid",
            external_id="eid",
            title="Implement feature X",
            description="Details about feature X",
            message_ids=["m1", "m2"],
            start_time="2024-07-01T10:00:00Z",
            end_time="2024-07-01T12:00:00Z",
            storypoints=5.0,
            assignees=["u1", "u2"],
            priority="high",
            parent_task=None,
            sub_tasks=[]
        )
        assert task.title == "Implement feature X"
        assert task.description == "Details about feature X"
        assert task.storypoints == 5.0
        assert task.assignees == ["u1", "u2"]
        assert task.priority == "high"
        assert task.sub_tasks == []

    def test_task_with_subtasks(self):
        """Test Task entity with nested sub_tasks."""
        sub = Task(
            chatmill_id="cmid2",
            title="Subtask",
            description="Subtask desc",
            message_ids=["m3"]
        )
        task = Task(
            chatmill_id="cmid",
            title="Parent",
            description="Parent desc",
            message_ids=["m1"],
            sub_tasks=[sub]
        )
        assert len(task.sub_tasks) == 1
        assert task.sub_tasks[0].title == "Subtask"

    def test_task_serialization(self):
        """Test serialization and deserialization of Task entity."""
        task = Task(
            chatmill_id="cmid",
            title="T",
            description="D",
            message_ids=["m1"]
        )
        data = task.dict()
        task2 = Task.parse_obj(data)
        assert task2 == task

    def test_task_missing_required(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(Exception):
            Task(title="T", description="D", message_ids=["m1"])  # missing chatmill_id 