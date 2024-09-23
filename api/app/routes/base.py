"""
Define words routes
"""
from flask import Blueprint, jsonify
# from celery.result import AsyncResult
# from app.tasks import add_together

# -----------------------------------------------------------------------------

base_bp = Blueprint('base', __name__, url_prefix='')

# -----------------------------------------------------------------------------


@base_bp.route('/health-check', methods=['GET'])
def health_check():
    return jsonify({'message': 'OK'}), 200


# @base_bp.route('/add/<int:param1>/<int:param2>')
# def add(param1: int, param2: int) -> str:
#     task = add_together.delay(param1, param2)

#     return jsonify({'id': task.id}), 200


# @base_bp.route('/check/<string:task_id>')
# def check_task(task_id: str) -> str:
#     result = AsyncResult(task_id)

#     return {
#         "ready": result.ready(),
#         "successful": result.successful(),
#         "value": result.result if result.ready() else None,
#     }
