import asyncio
from interfaces.schemas.event_schema import build_capture_event
from interfaces.api.to_missspec.capture import notify_missspec_capture
from infrastructure.platform.webhook_handler import get_webhook_url, set_webhook, send_webhook_message
from domain.value_objects.agent_profile import AgentProfile


async def handle_capture_command(interaction, message_ids, fetched_messages):
    """
    Orchestrate the full MissSpec capture business flow: build event, notify agent, echo webhook.
    Args:
        interaction: discord.Interaction
        message_ids: List[int]
        fetched_messages: List[Message]
    """
    # Build Capture event
    capture_event = build_capture_event(
        interaction=interaction,
        message_ids=message_ids,
        messages=fetched_messages,
    )
    # Notify Miss Spec agent
    await notify_missspec_capture(capture_event)
    # After response, send a webhook message to Discord
    agent_profile = capture_event.agent_profile
    webhook_url = await get_webhook_url(agent_profile.webhook_name, agent_profile.channel_id)
    if webhook_url is None:
        await set_webhook(agent_profile.webhook_name, agent_profile.channel_id, interaction.client)
    await send_webhook_message(
        agent_profile=agent_profile,
        content="Agent has received the capture event!"
    )
