from fastapi import FastAPI

app = FastAPI(title="Tevira-AI")

@app.get("/health")
def check_health():
    return {"status": "ok", "service": "tevira-ai"}