import pytest
from interfaces.schemas import supplement_request_embeds_schema
from domain.events.supplement_request import SupplementRequest
from domain.entities.spec import Spec

class DummyEmbed:
    def __init__(self, title, description=None, color=None):
        self.title = title
        self.description = description
        self.color = color
        self.fields = []
        self.footer = None
    def add_field(self, name, value, inline):
        self.fields.append((name, value, inline))
    def set_footer(self, text):
        self.footer = text


def test_build_discord_embeds_from_supplement_request(monkeypatch):
    # 用真实 SupplementRequest，mock discord.Embed
    spec = Spec(chatmill_id="cmid", message_ids=["m1"], title="t", description="d")
    req = SupplementRequest(session_id="sid", event_id="eid", operator_id="uid", payload=spec, history=[], question="cont")
    # dict 化
    req_dict = req.model_dump()
    req_dict["event_type"] = "supplement_request"
    req_dict["spec"] = spec.model_dump()
    # patch discord.Embed/Color
    monkeypatch.setattr(supplement_request_embeds_schema, "discord", type("discord", (), {"Embed": DummyEmbed, "Color": type("Color", (), {"purple": staticmethod(lambda: 1), "blue": staticmethod(lambda: 2)})}))
    embeds = supplement_request_embeds_schema.build_discord_embeds_from_supplement_request(req_dict)
    assert isinstance(embeds, list)
    assert len(embeds) == 2
    assert embeds[0].title == "📝 Supplement Request"
    assert "cont" in embeds[0].description
    assert embeds[1].title == "🗂️ Spec Info"
    assert "t" in embeds[1].description 