from celery import shared_task
from app.models import inspect_movement


@shared_task(ignore_result=False)
def remove_by_dtw(sensor_data) -> list[int]:
    bad_samples, threshold = inspect_movement(sensor_data)

    return {
        "bad_samples": bad_samples,
        "threshold": threshold,
    }
