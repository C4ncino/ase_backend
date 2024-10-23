from celery.result import AsyncResult
# from flask_jwt_extended import jwt_required
from flask import Blueprint, jsonify, request

from app.database import database
from app.utils import pp_decorator
from app.tasks import remove_by_dtw, train_models
from app.models import inspect_fingers


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

    if result.ready() and result.successful():
        bad_samples, threshold, centroid, radius = result.result

        return jsonify({
            "ready": result.ready(),
            "success": result.successful(),
            "result": {
                "bad_samples": bad_samples,
                "threshold": threshold,
                "centroid": centroid,
                "radius": radius
            },
        }), 200

    return jsonify({
        "ready": result.ready(),
        "success": result.successful(),
        "result": {
            "bad_samples": None,
            "threshold": None,
            "centroid": None,
            "radius": None
        },
    }), 200


@training_bp.route('', methods=['POST'])
@pp_decorator(request,
              required_fields=['sensor_data', 'word', 'user_id', 'chars'])
# @jwt_required()
def train():
    try:
        sensor_data = request.json['sensor_data']

        task = train_models.delay(sensor_data, {
            'user_id': request.json['user_id'],
            'word': request.json['word'],
            'characteristics': request.json['chars']
        })

        return jsonify({
            'task': task.id
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@training_bp.route('/<string:task_id>')
# @jwt_required()
def train_check(task_id):
    result = AsyncResult(task_id)

    if result.ready() and result.successful():
        db_info, sensor_data = result.result

        _, row = database.create_table_row('words', db_info)

        database.create_table_row('data_words', {
            'id_word': row.id,
            'data': sensor_data
        })

        return jsonify({
            "ready": result.ready(),
            "success": result.successful(),
            "word": row.serialize()
        }), 200

    return jsonify({
        "ready": result.ready(),
        "success": result.successful(),
        "word": None,
    }), 200
