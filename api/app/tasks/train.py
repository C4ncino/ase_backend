from celery import shared_task, states

from app.database import database
from app.models import inspect_movement, get_centroid
from app.models import SMALL_MODEL_POOL, LARGE_MODEL_POOL
from app.models import prepare_data, prepare_data_for_lm
from app.models import get_model, get_large_model
from app.models import calculate_metrics, has_better_metrics
from app.models import convert_model_to_tfjs


@shared_task(ignore_result=False)
def remove_by_dtw(sensor_data: list[dict]) -> list[int]:
    bad_samples, threshold = inspect_movement(sensor_data)

    for i in sorted(bad_samples, reverse=True):
        del sensor_data[i]

    _, centroid, radius = get_centroid(sensor_data)

    return bad_samples, threshold, centroid.tolist(), radius


@shared_task(ignore_result=False, bind=True)
def train_models(self, sensor_data: list[dict], db_info: dict) -> tuple[dict, dict, list[dict]]:
    best_model = None
    best_metrics = None

    user_id = db_info['user_id']

    x_train, x_val, y_train, y_val = prepare_data(sensor_data, user_id)

    self.update_state(
        state='PROGRESS',
        meta={
            'current': "getting first",
            'best': y_val.tolist()
        }
    )

    for model_version in SMALL_MODEL_POOL:

        model = get_model(model_version)

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

        metrics = calculate_metrics(y_val, y_pred, y_pred_prob)

        if metrics['roc_auc'] > 0.85:
            best_model = model
            best_metrics = metrics
            break

        if best_metrics is None:
            best_model = model
            best_metrics = metrics
            continue

        if has_better_metrics(metrics, best_metrics):
            best_model = model
            best_metrics = metrics

        self.update_state(
            state='PROGRESS',
            meta={
                'current': metrics,
                'best': best_metrics
            }
        )

    model_info = convert_model_to_tfjs(best_model)

    user_words = database.read_by_field('words', 'user_id', user_id)

    db_info['model'] = model_info

    db_info['class_key'] = len(user_words) + 1

    return db_info, sensor_data


@shared_task(ignore_result=False)
def train_large_model(user_id: int) -> dict:

    x_train, x_val, y_train, y_val, n_classes = prepare_data_for_lm(user_id)

    model = get_large_model('L1', n_classes + 1)

    model.fit(
        x_train,
        y_train,
        epochs=50,
        batch_size=16,
        validation_data=(x_val, y_val),
        verbose=0,
    )

    model_info = convert_model_to_tfjs(model)

    return model_info, user_id
