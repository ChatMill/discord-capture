from typing import Optional


class PublishResult:
    """
    Value object representing the result of a publish event.
    """

    def __init__(
            self,
            status: str,
            platform: str,
            url: Optional[str] = None,
            message: Optional[str] = None,
            id: Optional[str] = None
    ):
        self.status = status
        self.platform = platform
        self.url = url
        self.message = message
        self.id = id
