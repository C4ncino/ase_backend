from celery import shared_task

from app.models import inspect_movement, get_centroid
from app.models import prepare_data, MODEL_POOL
from app.models import calculate_metrics, compare_metrics
from app.models import convert_model_to_tfjs


@shared_task(ignore_result=False)
def remove_by_dtw(sensor_data: list[dict]) -> list[int]:
    bad_samples, threshold = inspect_movement(sensor_data)

    for i in sorted(bad_samples, reverse=True):
        del sensor_data[i]

    _, centroid, radius = get_centroid(sensor_data)

    return bad_samples, threshold, centroid, radius


@shared_task(ignore_result=True)
def train_models(sensor_data: list[dict], db_info: dict) -> dict:
    best_model = None
    best_metrics = None

    user_id = db_info['user_id']

    x_train, x_val, y_train, y_val = prepare_data(sensor_data, user_id)

    for _, model in MODEL_POOL.items():
        model.fit(
            x_train,
            y_train,
            epochs=20,
            batch_size=8,
            validation_data=(x_val, y_val),
            verbose=0
        )

        y_pred_prob = model.predict(x_val)
        y_pred = (y_pred_prob > 0.5).astype(int)

        metrics = calculate_metrics(y_val, y_pred)

        if best_metrics is None:
            best_model = model
            best_metrics = metrics
            continue

        if compare_metrics(metrics, best_metrics):
            best_model = model
            best_metrics = metrics

    model_info = convert_model_to_tfjs(best_model)

    return model_info, db_info, sensor_data
