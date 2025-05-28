import httpx

from domain.events.capture import Capture
from infrastructure.config.settings import get_agent_base_url, AgentServiceName


async def notify_missspec_capture(event: Capture) -> None:
    """
    Send a Capture event to the Miss Spec agent via HTTP POST.
    Args:
        event: The Capture event to send
    Raises:
        httpx.HTTPError: If the HTTP request fails
        httpx.TimeoutException: If the request times out
    """
    agent_url = get_agent_base_url(AgentServiceName.MISS_SPEC) + "/agent/missspec/capture"

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                agent_url,
                json=event.dict(),  # Use Pydantic's .dict() for serialization
                timeout=10.0
            )
            resp.raise_for_status()
            print(f"[notify_missspec_capture] Success: status={resp.status_code}")
    except httpx.TimeoutException as e:
        print(f"[notify_missspec_capture] Timeout: {str(e)}")
        raise
    except httpx.HTTPError as e:
        print(f"[notify_missspec_capture] HTTP Error: {str(e)}")
        raise
    except Exception as e:
        print(f"[notify_missspec_capture] Unexpected error: {str(e)}")
        raise
