from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
from mock.interfaces.schemas.capture2supplement_schema import build_supplement_request_from_capture

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "mock_agent"}


@app.post("/agent/webhook")
async def agent_webhook(request: Request):
    data = await request.json()
    print(f"[mock_agent] Received webhook: {data}")
    return {"received": True, "echo": data}


@app.post("/agent/missspec/capture")
async def receive_capture(request: Request):
    payload = await request.json()
    print("[mock_agent] Received Miss Spec capture event:", payload)

    # Build SupplementRequest using schema logic (async)
    supplement_request = await build_supplement_request_from_capture(payload)

    # Fire POST to main service
    url = "http://localhost:8101/capture/discord/supplement_request"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=supplement_request.dict(), timeout=10)
            print(f"[mock_agent] Fired supplement_request, status={resp.status_code}, resp={resp.text}")
    except Exception as e:
        print(f"[mock_agent] Failed to fire supplement_request: {e}")

    return JSONResponse(content={"status": "received"}, status_code=200)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8201)
