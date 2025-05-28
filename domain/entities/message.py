class Message:
    """
    Domain entity representing a Discord message, including author id and name.
    """

    def __init__(self, message_id: str, author_id: str, author_name: str, content: str, timestamp: str):
        self.id = message_id
        self.author_id = author_id
        self.author_name = author_name
        self.content = content
        self.timestamp = timestamp
