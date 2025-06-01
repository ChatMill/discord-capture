from infrastructure.platform.webhook_handler import get_webhook_url, set_webhook, send_webhook_message
from interfaces.api.to_missspec.capture import notify_missspec_capture  # 可后续拆分为 supplement 专用
from application.services.feedback_utils import agent_response_with_retry
from interfaces.api.to_missspec.supplement import notify_missspec_supplement

SUCCESS_FEEDBACK = (
    "🚀 Supplement received and sent to the agent! Awaiting response."
)
ERROR_FEEDBACK = (
    "❌ Failed to process supplement: {error_msg}\nPlease try again."
)
RETRY_FEEDBACKS = [
    "⏳ Still working on your supplement! Waiting for agent response...",
    "🕰️ Sorry for the wait! Still waiting for the agent's response.",
    "⚠️ The agent is taking too long to respond.\nError type: {error_type}\nDetails: {error_msg}"
]

async def handle_supplement_command(interaction, event):
    """
    Orchestrate the MissSpec supplement business flow: notify agent and echo webhook.
    Args:
        interaction: discord.Interaction
        event: Pre-built event object (e.g., Supplement)
    """
    agent_profile = event.agent_profile
    webhook_url = await get_webhook_url(agent_profile.webhook_name, agent_profile.channel_id)
    if webhook_url is None:
        await set_webhook(agent_profile.webhook_name, agent_profile.channel_id, interaction.client)
    await agent_response_with_retry(
        agent_profile=agent_profile,
        event=event,
        notify_func=notify_missspec_supplement,  # 可后续拆分为 supplement 专用 notify
        send_func=send_webhook_message,
        success_feedback=SUCCESS_FEEDBACK,
        error_feedback=ERROR_FEEDBACK,
        retry_feedbacks=RETRY_FEEDBACKS,
        max_retries=3,
        retry_interval=10
    ) 