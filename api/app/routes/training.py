from flask import Blueprint, jsonify, request
from app.utils import pp_decorator, inspect_fingers
# from flask_jwt_extended import jwt_required
from app.tasks import remove_by_dtw
from celery.result import AsyncResult


training_bp = Blueprint('training', __name__, url_prefix='/training')


@training_bp.route('')
def h_check():
    return jsonify({'success': True}), 200


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
                'error': 'Se requieren al menos 18 lecturas en sensor_data'
            }), 400

        fatly_samples, centroid = inspect_fingers(sensor_data)

        if len(fatly_samples) < 16:
            return jsonify({
                'success': False,
                'samples': fatly_samples.tolist()
            }), 400

        task = remove_by_dtw.delay(sensor_data)

        return jsonify({
            'success': True,
            'message': 'Verificando movimientos',
            'task': task.id,
            'samples': fatly_samples.tolist()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@training_bp.route('/validate/<string:task_id>')
# @jwt_required()
def validate_check(task_id):
    result = AsyncResult(task_id)

    return jsonify({
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }), 200
