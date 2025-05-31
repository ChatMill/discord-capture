import httpx
from fastapi import FastAPI, Request, BackgroundTasks

from interfaces.schemas.capture2supplement_schema import build_supplement_request_from_capture
from shared.agent_response import AgentResponse

app = FastAPI()

fail_count = 0  # Global counter for simulating failures


@app.get("/health")
async def health():
    return {"status": "ok", "service": "mock_agent"}


@app.post("/agent/webhook")
async def agent_webhook(request: Request):
    data = await request.json()
    print(f"[mock_agent] Received webhook: {data}")
    return {"received": True, "echo": data}


@app.post("/agent/missspec/capture")
async def receive_capture(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    print("[mock_agent] Received Miss Spec capture event:", payload)

    # Immediately reply with AgentResponse (success)
    response = AgentResponse(success=True, error=None, data={"status": "received"})

    # Background task: build and send supplement_request after sleep
    async def process_and_send():
        supplement_request = await build_supplement_request_from_capture(payload)
        import asyncio
        await asyncio.sleep(1.0)  # Simulate AI delay
        url = "http://discord-capture:8101/capture/discord/supplement_request"
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=supplement_request.dict(), timeout=10)
                print(f"[mock_agent] Fired supplement_request, status={resp.status_code}, resp={resp.text}")
        except Exception as e:
            print(f"[mock_agent] Failed to fire supplement_request: {e}")

    background_tasks.add_task(process_and_send)
    return response.dict()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8201)
