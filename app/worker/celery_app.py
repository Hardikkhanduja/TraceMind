from celery import Celery

from opentelemetry.instrumentation.celery import (
    CeleryInstrumentor,
)

celery_app = Celery(
    "tracemind",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=[
        "app.tasks.workflow_tasks",
    ],
)

CeleryInstrumentor().instrument()

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

CeleryInstrumentor().instrument()