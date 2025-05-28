from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "mock_publish"}


@app.post("/publish/webhook")
async def publish_webhook(request: Request):
    data = await request.json()
    print(f"[mock_publish] Received webhook: {data}")
    return {"received": True, "echo": data}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8301)
