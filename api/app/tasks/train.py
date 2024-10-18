from celery import shared_task
from app.models import inspect_movement, get_centroid, MODEL_POOL, calculate_metrics
from app.models import prepare_data, compare_metrics, save_model_as_tensorflowjs
from app.database import database
import numpy as np
import pandas as pd



@shared_task(ignore_result=False)
def remove_by_dtw(sensor_data: list[dict]) -> list[int]:
    bad_samples, threshold = inspect_movement(sensor_data)

    for i in sorted(bad_samples, reverse=True):
        del sensor_data[i]

    _, centroid, radius = get_centroid(sensor_data)




    # TODO: add info to database





@shared_task(ignore_result=True, bind=True)
def train_models(self, sensor_data: list[dict]):
    # TODO: Training with update

    # Inicializar variables para almacenar el mejor modelo y sus métricas
    best_model = None
    best_metrics = None

    # Preparar los datos para el entrenamiento y la validación
    X_train, X_val, y_train, y_val = prepare_data(sensor_data)

    # Probar cada modelo en el MODEL_POOL
    for _, model in MODEL_POOL.items():
        model.fit(
            X_train,
            y_train,
            epochs=20,
            batch_size=8,
            validation_data=(X_val, y_val),
            verbose=0  
        )

        # Obtener predicciones en el conjunto de validación
        y_pred_prob = model.predict(X_val)
        y_pred = (y_pred_prob > 0.5).astype(int)

        # Calcular las métricas para este modelo
        metrics = calculate_metrics(y_val, y_pred)

        if best_metrics is None:
            best_model = model
            best_metrics = metrics
            continue

        # Si es el primer modelo o tiene mejores métricas que el mejor hasta ahora, actualizar
        if compare_metrics(metrics, best_metrics):
            best_model = model
            best_metrics = metrics

    model_params = save_model_as_tensorflowjs(best_model)

    return model_params
