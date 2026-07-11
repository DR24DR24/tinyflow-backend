from fastapi import FastAPI
from pydantic import BaseModel
from celery.result import AsyncResult

from celery_app import celery_app

import socket


app = FastAPI(
    title="TinyFlow API",
    description="TinyML optimization platform MVP",
    version="0.1.0"
)


# -----------------------------
# Request models
# -----------------------------

class OptimizationRequest(BaseModel):
    model_name: str


# -----------------------------
# Health check
# -----------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "tinyflow-api",
        "host": socket.gethostname()
    }


# -----------------------------
# Root endpoint
# -----------------------------

@app.get("/")
def root():
    return {
        "project": "TinyFlow",
        "message": "API is running",
        "version": "0.1.0",
        "host": socket.gethostname()
    }


# -----------------------------
# Create optimization task
# -----------------------------

@app.post("/optimize")
def optimize(request: OptimizationRequest):

    task = celery_app.send_task(
        "tasks.optimize_model",
        args=[
            request.model_name
        ]
    )

    return {
        "task_id": task.id,
        "model": request.model_name,
        "status": "queued"
    }


# -----------------------------
# Task status
# -----------------------------

@app.get("/tasks/{task_id}")
def task_status(task_id: str):

    result = AsyncResult(
        task_id,
        app=celery_app
    )

    response = {
        "task_id": task_id,
        "status": result.status
    }

    if result.ready():
        response["result"] = result.result

    return response