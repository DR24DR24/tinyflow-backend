import time
import socket

from celery_app import celery_app


@celery_app.task(
    name="tasks.optimize_model"
)
def optimize_model(model_name: str):

    worker = socket.gethostname()

    print(
        f"Starting optimization: {model_name}"
    )

    print(
        f"Worker: {worker}"
    )


    # Имитация тяжелой операции:
    # анализ модели,
    # quantization,
    # benchmark и т.д.
    time.sleep(30)


    result = {
        "model": model_name,
        "worker": worker,
        "status": "completed",
        "message": "Optimization finished"
    }


    print(result)

    return result