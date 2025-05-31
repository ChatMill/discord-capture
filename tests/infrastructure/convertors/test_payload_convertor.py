import pytest
from infrastructure.convertors.payload_convertor import PayloadConvertor
from domain.entities.payload import Payload
from infrastructure.persistence.payload_document import PayloadDocument

def test_to_document():
    payload = Payload(
        chatmill_id="cmid",
        external_id=None,
        message_ids=["m1", "m2"]
    )
    doc = PayloadConvertor.to_document(payload)
    assert doc.payload_id == payload.chatmill_id
    assert doc.type == "Payload"
    # data 允许 None 字段
    assert doc.data == {"external_id": None, "message_ids": ["m1", "m2"]}

def test_to_entity():
    doc = PayloadDocument(
        payload_id="cmid",
        type="Payload",
        data={"message_ids": ["m1", "m2"]}
    )
    def payload_cls(id=None, chatmill_id=None, external_id=None, message_ids=None):
        # 兼容 PayloadConvertor.to_entity 的参数展开
        return Payload(chatmill_id=chatmill_id or id, external_id=external_id, message_ids=message_ids)
    entity = PayloadConvertor.to_entity(doc, payload_cls)
    assert isinstance(entity, Payload)
    assert entity.chatmill_id == "cmid"
    assert entity.message_ids == ["m1", "m2"] 