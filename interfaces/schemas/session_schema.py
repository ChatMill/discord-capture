from domain.entities.session import Session
from domain.value_objects.source import Source
from domain.entities.spec import Spec
from domain.events.base_event import Event


def build_session(source: Source, spec: Spec, event: Event, session_id: str):
    """
    Build a Session object from source, spec, and event.
    Uses the provided session_id for both Session and Event.
    Returns the new Session.
    """
    session = Session(
        session_id=session_id,
        source=source,
        history=[event.event_id],
        agent="missspec",
        payload=spec
    )
    return session
