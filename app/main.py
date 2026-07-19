from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.api.routers.health import router as health_router
from app.api.routers.workflow import router as workflow_router
from opentelemetry.instrumentation.celery import CeleryInstrumentor


CeleryInstrumentor().instrument()
app = FastAPI(
    title="TraceMind API",
    version="1.0.0",
    description="AI SRE for AI Agents"
)

app.include_router(health_router)
app.include_router(workflow_router)

FastAPIInstrumentor.instrument_app(app)