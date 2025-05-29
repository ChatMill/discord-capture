from domain.entities.session import Session
from domain.value_objects.source import Source
from domain.entities.task import Task
from domain.events.base_event import Event


def build_session(source: Source, task: Task, event: Event):
    """
    Build a Session object from source, task, and event.
    Assigns session_id to event, and appends event_id to session history.
    Returns the new Session and the updated Event.
    """
    session_id = source.session_id if hasattr(source, 'session_id') else f"session-{source.organization_id}-{source.project_id}"
    event.session_id = session_id
    session = Session(
        session_id=session_id,
        source=source,
        history=[event.event_id],
        agent="missspec",
        payload=task
    )
    return session
