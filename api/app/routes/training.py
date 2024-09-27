from celery.result import AsyncResult
# from flask_jwt_extended import jwt_required
from flask import Blueprint, jsonify, request

from app.utils import pp_decorator
from app.tasks import remove_by_dtw
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

    for i in bad_samples:
        sensor_data.pop(i)

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
    pass
