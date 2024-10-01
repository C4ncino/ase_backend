from celery import shared_task
from app.models import inspect_movement, get_centroid
# from app.database import database


@shared_task(ignore_result=False)
def remove_by_dtw(sensor_data: list[dict]) -> list[int]:
    bad_samples, threshold = inspect_movement(sensor_data)

    for i in sorted(bad_samples, reverse=True):
        del sensor_data[i]

    _, centroid, radius = get_centroid(sensor_data)

    # TODO: add info to database

    return bad_samples
