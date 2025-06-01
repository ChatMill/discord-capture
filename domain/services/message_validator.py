from typing import List, Tuple, Any
from domain.entities.message import Message


class MessageValidator:
    """
    Utility class for validating, deduplicating, and handling message fetch results in the capture flow.
    Handles missing message ids, deduplication, and provides helper methods for reply formatting.
    """

    @staticmethod
    def deduplicate_message_ids(message_ids: List[str]) -> List[str]:
        """
        Remove duplicate message ids while preserving order.
        """
        seen = set()
        deduped = []
        for mid in message_ids:
            if mid not in seen:
                deduped.append(mid)
                seen.add(mid)
        return deduped

    @staticmethod
    async def fetch_and_validate(
            message_ids: List[str],
            fetcher: Any,
            channel_id: str
    ) -> Tuple[List[Message], List[str]]:
        """
        Fetch messages by ids, return (found_messages, not_found_ids).
        Only found messages are returned as Message entities.
        """
        deduped_ids = MessageValidator.deduplicate_message_ids(message_ids)
        fetched_messages = await fetcher.fetch_messages(channel_id, deduped_ids)
        found_ids = {m.id for m in fetched_messages}
        not_found_ids = [mid for mid in deduped_ids if mid not in found_ids]
        return fetched_messages, not_found_ids

    @staticmethod
    def format_not_found_message(not_found_ids: List[str]) -> str:
        """
        Format a friendly string listing not found message ids, or empty string if all found.
        """
        if not not_found_ids:
            return ""
        return f"Sorry, I couldn't find these message(s): {', '.join(not_found_ids)}.\n"
