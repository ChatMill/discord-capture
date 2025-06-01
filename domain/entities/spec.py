from typing import List, Optional, Dict

from pydantic import BaseModel

from domain.entities.payload import Payload


class Spec(Payload, BaseModel):
    """
    Spec entity for Miss Spec agent, representing a structured requirement or sub-spec.
    Inherits from Payload and Pydantic BaseModel.

    Each field is annotated with its meaning and mapping to GitHub/Jira/Notion concepts.
    """

    external_id: Optional[str] = None  # External system id (e.g., GitHub issue id, Jira issue id)
    title: str  # Title of the spec (GitHub/Jira: title/summary)
    description: str  # Detailed description (GitHub: body, Jira: description)
    message_ids: List[str]  # Related message ids (custom, for traceability)
    start_time: Optional[str] = None  # Start time (Jira: custom field, Notion: date property)
    end_time: Optional[str] = None  # End time (Jira: due date, Notion: date property)
    storypoints: Optional[float] = None  # Effort estimation (Jira: story points, GitHub: estimate via projects)
    assignees: List[str] = []  # Responsible users (GitHub/Jira: assignees)
    priority: Optional[str] = None  # Priority level (Jira: priority, GitHub: label)
    parent_spec: Optional[str] = None  # Parent spec id (Jira: epic link, GitHub: parent issue)
    sub_specs: List['Spec'] = []  # Sub-specs (Jira: sub-tasks, GitHub: task list)
    created_at: Optional[str] = None  # Creation timestamp (GitHub/Jira: created_at)
    updated_at: Optional[str] = None  # Last update timestamp (GitHub/Jira: updated_at)
    created_by: Optional[str] = None  # Creator (GitHub/Jira: author/reporter)
    updated_by: Optional[str] = None  # Last modifier (GitHub/Jira: last editor)
    status: Optional[str] = None  # Current status (GitHub: open/closed, Jira: to-do/in progress/done)
    tags: List[str] = []  # Tags or labels (GitHub: labels, Jira: labels)
    attachments: List[str] = []  # Attachment URLs (GitHub: attachments, Jira: attachments)
    acceptance_criteria: Optional[str] = None  # Acceptance criteria (Jira: AC, Notion: custom field)
    comments: List[str] = []  # Comments or discussion (GitHub/Jira: comments)
    related_specs: List[str] = []  # Related specs/issues (GitHub: linked issues, Jira: issue links)
    type: Optional[str] = None  # Type of spec (feature/bug/task/doc) (GitHub: label, Jira: issue type)
    actor: Optional[str] = None  # The actor/user role for this spec (Jira: custom field, Notion: property)
    trigger: Optional[str] = None  # The trigger/event for this spec (Jira: custom field, Notion: property)
    flow: Optional[str] = None  # The flow/scenario for this spec (Jira: custom field, Notion: property)
    custom_fields: Optional[Dict[str, str]] = None  # Custom fields for extensibility (Jira/Notion: custom fields)
