import uvicorn
from fastapi import FastAPI
from api.monitor import router as monitor_router
from api.evaluate import router as evaluate_router
from api.report import router as report_router
from core.config import HOST, PORT

app = FastAPI(title="AgentOps LLM Observability & Evaluation Platform MVP")

# Include the routers for API endpoints
app.include_router(monitor_router)
app.include_router(evaluate_router)
app.include_router(report_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "AgentOps Observability & Evaluation Platform API"
    }

if __name__ == "__main__":
    # Start the server on configured host and port
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
