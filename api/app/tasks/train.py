from celery import shared_task
from utils import inspect_movement


@shared_task(ignore_result=False)
def remove_by_dtw(sensor_data) -> list[int]:
    results = inspect_movement(sensor_data)

    return results
