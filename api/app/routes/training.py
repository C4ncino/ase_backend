from flask import Blueprint, jsonify, request
from app.utils import pp_decorator, inspect_fingers
# from flask_jwt_extended import jwt_required
from app.tasks import remove_by_dtw
from celery.result import AsyncResult


training_bp = Blueprint('training', __name__, url_prefix='/train')


@training_bp.route('/validate', methods=['POST'])
@pp_decorator(request, required_fields=['sensor_data'])
# @jwt_required()
def validate_training():
    try:
        data = request.json

        sensor_data = data.get('sensor_data')

        if not sensor_data or not isinstance(sensor_data, list):
            return jsonify({'error': 'sensor_data debe ser una lista'}), 400

        if len(sensor_data) < 18:
            return jsonify({
                'error': 'Se requieren al menos 20 lecturas en sensor_data'
            }), 400

        bad_samples, centroid = inspect_fingers(sensor_data)

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
            'centroid': centroid,
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@training_bp.route('/validate/<string:task_id>')
@pp_decorator(request, required_fields=['sensor_data', 'centroid'])
# @jwt_required()
def validate_check(task_id):
    result = AsyncResult(task_id)

    return jsonify({
        "ready": result.ready(),
        "success": result.successful(),
        "result": result.result if result.ready() else None,
    }), 200


@training_bp.route('', methods=['POST'])
def train():
    pass