import pytest
from domain.entities.spec import Spec

class TestSpec:
    """
    Unit tests for the Spec entity.
    """
    def test_spec_creation(self):
        """Test creating a Spec entity with all fields."""
        spec = Spec(
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
            parent_spec=None,
            sub_specs=[]
        )
        assert spec.title == "Implement feature X"
        assert spec.description == "Details about feature X"
        assert spec.storypoints == 5.0
        assert spec.assignees == ["u1", "u2"]
        assert spec.priority == "high"
        assert spec.sub_specs == []

    def test_spec_with_subspecs(self):
        """Test Spec entity with nested sub_specs."""
        sub = Spec(
            chatmill_id="cmid2",
            title="Subspec",
            description="Subspec desc",
            message_ids=["m3"]
        )
        spec = Spec(
            chatmill_id="cmid",
            title="Parent",
            description="Parent desc",
            message_ids=["m1"],
            sub_specs=[sub]
        )
        assert len(spec.sub_specs) == 1
        assert spec.sub_specs[0].title == "Subspec"

    def test_spec_serialization(self):
        """Test serialization and deserialization of Spec entity."""
        spec = Spec(
            chatmill_id="cmid",
            title="T",
            description="D",
            message_ids=["m1"]
        )
        data = spec.dict()
        spec2 = Spec.parse_obj(data)
        assert spec2 == spec

    def test_spec_missing_required(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(Exception):
            Spec(title="T", description="D", message_ids=["m1"])  # missing chatmill_id