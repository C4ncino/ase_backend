from datetime import datetime as dt
from celery.result import AsyncResult
# from flask_jwt_extended import jwt_required
from flask import Blueprint, jsonify, request

from app.database import database
from app.utils import pp_decorator
from app.tasks import remove_by_dtw, train_models, train_large_model
from app.models import inspect_fingers, prepare_data, prepare_data_for_lm


training_bp = Blueprint('training', __name__, url_prefix='/train')


@training_bp.route('/validate', methods=['POST'])
@pp_decorator(request, required_fields=['sensor_data'])
# @jwt_required()
def validate_data():
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

    response = {
        "bad_samples": None,
        "threshold": None,
        "centroid": None,
        "radius": None
    }

    if result.ready() and result.successful():
        bad_samples, threshold, centroid, radius = result.result

        response['bad_samples'] = bad_samples
        response['threshold'] = threshold
        response['centroid'] = centroid
        response['radius'] = radius

    return jsonify({
        "ready": result.ready(),
        "success": result.successful(),
        "result": response,
    }), 200


@training_bp.route('', methods=['POST'])
@pp_decorator(request,
              required_fields=['sensor_data', 'word', 'user_id', 'chars'])
# @jwt_required()
def train():
    # try:
    sensor_data = request.json['sensor_data']

    user_id = request.json['user_id']

    x_train, x_val, y_train, y_val = prepare_data(sensor_data, user_id)

    task = train_models.delay({
        'xTrain': x_train.tolist(),
        'xVal': x_val.tolist(),
        'yTrain': y_train.tolist(),
        'yVal': y_val.tolist()
    }, {
        'user_id': request.json['user_id'],
        'word': request.json['word'],
        'characteristics': request.json['chars']
    }, sensor_data)

    return jsonify({
        'task': task.id
    }), 200

    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500


@training_bp.route('/<string:task_id>')
# @jwt_required()
def train_check(task_id):
    result = AsyncResult(task_id)

    if result.ready() and result.successful():
        db_info, sensor_data = result.result

        user_id = db_info['user_id']

        user_words = database.read_by_field('words', 'user_id', user_id)

        db_info['class_key'] = len(user_words)

        _, row = database.create_table_row('words', db_info)

        database.create_table_row('data_words', {
            'id': row.id,
            'data': sensor_data
        })

        user_id = db_info['user_id']

        x_train, x_val, y_train, y_val, n_classes = prepare_data_for_lm(user_id)

        train_task = train_large_model.delay(
            {
                'xTrain': x_train.tolist(),
                'xVal': x_val.tolist(),
                'yTrain': y_train.tolist(),
                'yVal': y_val.tolist()
            },
            n_classes,
            user_id
        )

        return jsonify({
            "ready": result.ready(),
            "success": result.successful(),
            "word": row.serialize(),
            "train_large_task": train_task.id,
        }), 200

    return jsonify({
        "ready": result.ready(),
        "success": result.successful(),
        "word": None,
        "train_large_task": None,
    }), 200


@training_bp.route('/large-model/<string:task_id>')
# @jwt_required()
def validate_train_large(task_id):
    result = AsyncResult(task_id)
    row = None

    if result.ready() and result.successful():
        model_info, user_id = result.result

        existing_model = database.read_by_id('models', user_id)

        if existing_model:
            row = database.update_table_row(
                'models',
                user_id,
                {'model': model_info, 'last_update': dt.now()}
            )
        else:
            _, row = database.create_table_row(
                'models',
                {'id': user_id, 'model': model_info}
            )

    return jsonify({
        "ready": result.ready(),
        "success": result.successful(),
        "result": row.serialize() if row else None,
    }), 200
