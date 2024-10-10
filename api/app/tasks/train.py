from celery import shared_task
from app.models import inspect_movement, get_centroid, MODEL_POOL, calculate_metrics
# from app.database import database
from tensorflow.keras.models import Model
import numpy as np
import pandas as pd



@shared_task(ignore_result=False)
def remove_by_dtw(sensor_data: list[dict]) -> list[int]:
    bad_samples, threshold = inspect_movement(sensor_data)

    for i in sorted(bad_samples, reverse=True):
        del sensor_data[i]

    _, centroid, radius = get_centroid(sensor_data)

    # TODO: add info to database

    return bad_samples


@shared_task(ignore_result=True, bind=True)
def train(self, sensor_data: list[dict], word: str):
    # TODO: Training with update

    # Inicializar variables para almacenar el mejor modelo y sus métricas
    best_model = None
    best_metrics = None
    best_model_name = None

    # Probar cada modelo en el MODEL_POOL
    for model_name, model in MODEL_POOL.items():

        # Preparar los datos para el entrenamiento y la validación
        X_train, X_val, y_train, y_val = prepare_data(sensor_data, word)

        # Entrenar el modelo
        history = model.fit(
            X_train,
            y_train,
            epochs=20,
            batch_size=8,
            validation_data=(X_val, y_val),
            verbose=0  
        )

        # Obtener predicciones en el conjunto de validación
        y_pred = model.predict(X_val)
        y_pred = (y_pred > 0.5).astype(int)

        # Calcular las métricas para este modelo
        metrics = calculate_metrics(y_val, y_pred)

        # Si es el primer modelo o tiene mejores métricas que el mejor hasta ahora, actualizar
        if best_metrics is None or compare_metrics(metrics, best_metrics):
            best_model = model
            best_metrics = metrics
            best_model_name = model_name

    # Guardar el mejor modelo
    if best_model:
        save_model(best_model, best_model_name)


def prepare_data(sensor_data: list[dict], word: str):
    n_samples = len(data)
    data = np.array([pd.DataFrame(i).values for i in sensor_data])
    labels = np.array([1]*n_samples)

    train_size = int(0.8 * n_samples)
    indices = np.random.permutation(n_samples)
    train_indices, val_indices = indices[:train_size], indices[train_size:]
    X_train, X_val = data[train_indices], data[val_indices]
    y_train, y_val = labels[train_indices], labels[val_indices]
    return X_train, X_val, y_train, y_val

def compare_metrics(metrics, best_metrics):
    return metrics['f1_score'] > best_metrics['f1_score']


def save_model(model: Model, model_name: str, metrics):
    model.save(f'model_{model_name}.h5')
    with open(f'metrics_{model_name}.json', 'w') as f:
        import json
        json.dump(metrics, f)

    print(f"Mejor modelo guardado: {model_name}")
    print("Métricas:", metrics)
