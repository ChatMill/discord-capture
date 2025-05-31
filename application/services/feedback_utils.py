import asyncio
import httpx
from typing import Callable, Any


async def agent_response_with_retry(
    agent_profile: Any,
    event: Any,
    notify_func: Callable[[Any], Any],
    send_func: Callable[[Any, str], Any],
    success_feedback: str,
    error_feedback: str,
    retry_feedbacks: list,
    max_retries: int = 3,
    retry_interval: int = 10
):
    """
    Notify agent with retries and send user feedback based on response.
    Args:
        agent_profile: The agent profile object for sending feedback.
        event: The event object to send to agent.
        notify_func: The async function to notify agent (should return AgentResponse).
        send_func: The async function to send feedback (e.g., send_webhook_message).
        success_feedback: The message to send on success.
        error_feedback: The message template to send on error (use {error_msg}).
        retry_feedbacks: List of retry feedback messages.
        max_retries: Maximum retry attempts.
        retry_interval: Seconds to wait between retries.
    """
    last_error = None
    for i in range(max_retries):
        try:
            resp = await notify_func(event)
            if not resp.success or (resp.error is not None and resp.error != ""):
                error_msg = resp.error or "Unknown error"
                user_msg = error_feedback.format(error_msg=error_msg)
                await send_func(agent_profile=agent_profile, content=user_msg)
                return
            await send_func(agent_profile=agent_profile, content=success_feedback)
            return
        except (httpx.TimeoutException, httpx.HTTPError, Exception) as e:
            last_error = e
            if i < max_retries - 1:
                await asyncio.sleep(retry_interval)
                await send_func(
                    agent_profile=agent_profile,
                    content=retry_feedbacks[i]
                )
            else:
                error_type = type(last_error).__name__
                error_msg = str(last_error)
                if isinstance(last_error, httpx.HTTPStatusError):
                    try:
                        agent_resp = last_error.response.text
                        error_msg = agent_resp[:200]
                    except Exception:
                        pass
                user_msg = retry_feedbacks[-1].format(error_type=error_type, error_msg=error_msg)
                await send_func(
                    agent_profile=agent_profile,
                    content=user_msg
                ) 