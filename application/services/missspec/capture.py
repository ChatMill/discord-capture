from infrastructure.platform.webhook_handler import get_webhook_url, set_webhook, send_webhook_message
from interfaces.api.to_missspec.capture import notify_missspec_capture
import asyncio
import httpx
from application.services.feedback_utils import agent_response_with_retry

# User-facing feedback messages (for maintainability and i18n)
SUCCESS_FEEDBACK = (
    "🚀 Whoosh! Your capture just landed in my creative workshop. "
    "I'm processing it faster than you can say \"Miss Spec\"! Stay tuned for the magic!"
)
ERROR_FEEDBACK = (
    "❌ Oh no! I tried to work my magic, but hit a snag: {error_msg}\n"
    "Let's double-check and try again!"
)
RETRY_FEEDBACKS = [
    "⏳ Still working on your capture! My creative gears are spinning, but the agent hasn't replied yet. Hang tight, magic takes time!",
    "🕰️ Sorry for the wait! My creative workshop is a bit busier than usual. I'm still waiting for the agent's response. Thanks for your patience!",
    "⚠️ Oops, the agent is taking too long to respond.\nError type: {error_type}\nDetails: {error_msg}"
]


async def handle_capture_command(interaction, event):
    """
    Orchestrate the MissSpec capture business flow: notify agent and echo webhook.
    Args:
        interaction: discord.Interaction
        event: Pre-built event object (e.g., Capture)
    """
    agent_profile = event.agent_profile
    webhook_url = await get_webhook_url(agent_profile.webhook_name, agent_profile.channel_id)
    if webhook_url is None:
        await set_webhook(agent_profile.webhook_name, agent_profile.channel_id, interaction.client)
    await agent_response_with_retry(
        agent_profile=agent_profile,
        event=event,
        notify_func=notify_missspec_capture,
        send_func=send_webhook_message,
        success_feedback=SUCCESS_FEEDBACK,
        error_feedback=ERROR_FEEDBACK,
        retry_feedbacks=RETRY_FEEDBACKS,
        max_retries=3,
        retry_interval=10
    )
