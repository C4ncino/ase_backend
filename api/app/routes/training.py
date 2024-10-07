from celery.result import AsyncResult
# from flask_jwt_extended import jwt_required
from flask import Blueprint, jsonify, request
from app.database import DatabaseInterface  

from app.utils import pp_decorator
from app.tasks import remove_by_dtw
from app.models import inspect_fingers

#MODEL
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import pandas as pd
import base64
import os
import tempfile





training_bp = Blueprint('training', __name__, url_prefix='/train')


@training_bp.route('/validate', methods=['POST'])
@pp_decorator(request, required_fields=['sensor_data'])
# @jwt_required()
def validate_training():
    data = request.json

    sensor_data = data.get('sensor_data')

    if not sensor_data or not isinstance(sensor_data, list):
        return jsonify({'error': 'sensor_data debe ser una lista'}), 400

    if len(sensor_data) < 18:
        return jsonify({
            'error': 'Se requieren al menos 18 lecturas en sensor_data'
        }), 400

    bad_samples = inspect_fingers(sensor_data)

    if len(bad_samples) > 5:
        return jsonify({
            'success': False,
            'samples': bad_samples
        }), 200

    for i in sorted(bad_samples, reverse=True):
        del sensor_data[i]

    task = remove_by_dtw.delay(sensor_data)

    return jsonify({
        'success': True,
        'task': task.id,
        'samples': bad_samples,
    }), 200


@training_bp.route('/validate/<string:task_id>')
# @jwt_required()
def validate_check(task_id):
    result = AsyncResult(task_id)

    return jsonify({
        "ready": result.ready(),
        "success": result.successful(),
        "bad_samples": result.result if result.ready() else None,
    }), 200


@training_bp.route('', methods=['POST'])
@pp_decorator(request, required_fields=['sensor_data'])
def train():
    try:

        sensor_data = request.json['sensor_data']
        data = np.array([pd.DataFrame(i).values for i in sensor_data])
        labels = np.array([1] * 15 + [0] * 34)

        n_samples, timesteps, features = data.shape

        n_samples = len(data)
        train_size = int(0.8 * n_samples)
        indices = np.random.permutation(n_samples)
        train_indices, val_indices = indices[:train_size], indices[train_size:]

        X_train, X_val = data[train_indices], data[val_indices]
        y_train, y_val = labels[train_indices], labels[val_indices]

        # Definir, compilar y entrenar el modelo LSTM 
        model = Sequential()
        model.add(LSTM(32, input_shape=(timesteps, features), return_sequences=True))
        model.add(LSTM(16))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        model.fit(X_train, y_train, epochs=20, batch_size=10, validation_data=(X_val, y_val))

         # Crear un archivo temporal para guardar el modelo
        with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as tmp_file:
            model_path = tmp_file.name
            model.save(model_path) 

        # Leer el contenido del archivo temporal
        with open(model_path, 'rb') as f:
            model_content = f.read()

         # Guardar la representación en base64 en la base de datos
        # model_instance = Model(
        #     filename='lstm_model.h5',
        #     file_data=model_base64  # Almacena la representación base64 del archivo
        # )

        # db = DatabaseInterface()
        # db.create_table_row(model_instance)

        model_base64 = base64.b64encode(model_content).decode('utf-8')
        
        os.remove(model_path)

        return jsonify({"model": model_base64, "samples": n_samples, "timestpes": timesteps, "feat": features}), 200
    
    except Exception as e:
        return jsonify({'error' : str(e)}),500
    
