from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

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
    return JSONResponse(content={"status": "received"}, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8201)
