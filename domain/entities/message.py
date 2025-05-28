class Message:
    """
    Domain entity representing a Discord message, including author id and name.
    """

    id: str
    author_id: str
    author_name: str
    content: str
    timestamp: str

    def __init__(self, message_id: str, author_id: str, author_name: str, content: str, timestamp: str):
        self.id = message_id
        self.author_id = author_id
        self.author_name = author_name
        self.content = content
        self.timestamp = timestamp

    def to_dict(self) -> dict:
        """
        Serialize the Message entity to a dictionary for JSON serialization.
        """
        return {
            "message_id": self.id,
            "author_id": self.author_id,
            "author_name": self.author_name,
            "content": self.content,
            "timestamp": self.timestamp,
        }
