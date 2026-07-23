from fastapi import FastAPI, Request
from pydantic import BaseModel

import time
import boto3
import os
import json
import uuid
import socket


app = FastAPI(
    title="TinyFlow API",
    description="TinyML optimization platform MVP",
    version="0.1.0"
)


# ==================================================
# AWS CLIENTS
# ==================================================

cloudwatch = boto3.client(
    "cloudwatch",
    region_name=os.getenv(
        "AWS_REGION",
        "eu-central-1"
    )
)


sqs = boto3.client(
    "sqs",
    region_name=os.getenv(
        "AWS_REGION",
        "eu-central-1"
    )
)


QUEUE_URL = os.getenv("QUEUE_URL")


# ==================================================
# LAST REQUEST METRIC
# ==================================================

@app.middleware("http")
async def update_last_request_time(
    request: Request,
    call_next
):

    response = await call_next(request)

    try:

        cloudwatch.put_metric_data(

            Namespace="TinyFlow/API",

            MetricData=[

                {
                    "MetricName": "LastRequestTime",

                    "Value": time.time(),

                    "Unit": "Seconds"
                }

            ]

        )

    except Exception as e:

        print(
            f"CloudWatch metric error: {e}"
        )


    return response



# ==================================================
# REQUEST MODELS
# ==================================================

class OptimizationRequest(BaseModel):

    model_name: str



# ==================================================
# HEALTH
# ==================================================

@app.get("/health")
def health():

    return {

        "status": "ok",

        "service": "tinyflow-api",

        "host": socket.gethostname()

    }



# ==================================================
# ROOT
# ==================================================

@app.get("/")
def root():

    return {

        "project": "TinyFlow",

        "message": "API is running",

        "version": "0.1.0",

        "host": socket.gethostname()

    }



# ==================================================
# CREATE OPTIMIZATION TASK
# ==================================================

@app.post("/optimize")
def optimize(
    request: OptimizationRequest
):

    task_id = str(uuid.uuid4())


    message = {

        "task_id": task_id,

        "model_name": request.model_name,

        "status": "queued",

        "created_at": time.time()

    }


    try:

        sqs.send_message(

            QueueUrl=QUEUE_URL,

            MessageBody=json.dumps(message)

        )


    except Exception as e:

        return {

            "status": "error",

            "message": str(e)

        }


    return {

        "task_id": task_id,

        "model": request.model_name,

        "status": "queued"

    }


# ==================================================
# TASK STATUS
# Пока заглушка
# Worker добавим позже
# ==================================================

@app.get("/tasks/{task_id}")
def task_status(task_id: str):

    return {
        "task_id": task_id,
        "status": "completed",
        "result": {
            "worker": "mock-worker",
            "finished_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    }



