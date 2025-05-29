from infrastructure.platform.webhook_handler import get_webhook_url, set_webhook, send_webhook_message
from interfaces.api.to_missspec.capture import notify_missspec_capture


async def handle_capture_command(interaction, event):
    """
    Orchestrate the MissSpec capture business flow: notify agent and echo webhook.
    Args:
        interaction: discord.Interaction
        event: Pre-built event object (e.g., Capture)
    """
    # Notify Miss Spec agent
    await notify_missspec_capture(event)
    # After response, send a webhook message to Discord
    agent_profile = event.agent_profile
    webhook_url = await get_webhook_url(agent_profile.webhook_name, agent_profile.channel_id)
    if webhook_url is None:
        await set_webhook(agent_profile.webhook_name, agent_profile.channel_id, interaction.client)
    await send_webhook_message(
        agent_profile=agent_profile,
        content='🚀 Whoosh! Your capture just landed in my creative workshop. '
                'I\'m processing it faster than you can say "Miss Spec"! Stay tuned for the magic!'
    )
