from celery import shared_task

from app.models import inspect_movement, get_centroid


@shared_task(ignore_result=False)
def remove_by_dtw(sensor_data: list[dict]) -> list[int]:
    bad_samples, threshold = inspect_movement(sensor_data)

    for i in sorted(bad_samples, reverse=True):
        del sensor_data[i]

    _, centroid, radius = get_centroid(sensor_data)

    return bad_samples, threshold, centroid.tolist(), radius


@shared_task(ignore_result=False, name='train_models')
def train_models(training_data: dict, db_info: dict, sensor_data: list[dict]) -> tuple[dict, list[dict]]:
    pass


@shared_task(ignore_result=False, name='train_large_model')
def train_large_model(training_data: dict, n_classes: int, user_id: int) -> tuple[dict, int]:
    pass
