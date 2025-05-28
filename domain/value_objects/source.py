from typing import List


class Source:
    """
    Value object representing the source context of a session (platform, org, channel, etc.).
    """

    def __init__(
            self,
            platform: str,
            organization_id: str,
            project_id: str,
            message_ids: List[int],
            participants: List[str]
    ):
        self.platform = platform
        self.organization_id = organization_id
        self.project_id = project_id
        self.message_ids = message_ids
        self.participants = participants
