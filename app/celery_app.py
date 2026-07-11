import os

from celery import Celery
from dotenv import load_dotenv


load_dotenv()


REDIS_HOST = os.getenv(
    "REDIS_HOST",
    "localhost"
)

REDIS_PORT = os.getenv(
    "REDIS_PORT",
    "6379"
)


REDIS_URL = (
    f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
)


celery_app = Celery(
    "tinyflow",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "tasks"
    ]
)


celery_app.conf.update(

    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],

    timezone="UTC",
    enable_utc=True,

    result_expires=3600,
)