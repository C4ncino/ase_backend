import datetime as dt
from app.database import database
from app.utils import pp_decorator
from flask import Blueprint, jsonify, request

models_bp = Blueprint('models', __name__, url_prefix='/models')


@models_bp.route('/check_version/<int:user_id>', methods=['POST'])
@pp_decorator(request, required_fields=['date'])
# @jwt_required()
def check_model_version(user_id):
    try:
        request_data = request.json
        request_date_str = request_data.get('date')

        request_date = dt.datetime.strptime(request_date_str, "%d-%m-%Y %H:%M:%S")

        latest_model = database.read_by_field('models', 'id', user_id)[0]

        if not latest_model:
            return jsonify(
                {'error': 'No se encontró ningún modelo para este usuario.'}
            ), 404

        latest_model_date = latest_model.last_update

        is_updated = latest_model_date <= request_date

        if is_updated:
            formatted_date = latest_model_date.strftime("%d-%m-%Y %H:%M:%S")

            return jsonify({
                'updated': True,
                'latest_version_date': formatted_date
            }), 200
        else:
            return jsonify({
                'updated': False,
                'latest_model': latest_model.serialize()
            }), 200

    except Exception as e:
        return jsonify(
            {'error': f'Error al procesar la solicitud: {str(e)}'}
        ), 500


@models_bp.route('/<int:user_id>', methods=['PUT'])
# @jwt_required()
def update_model(user_id):
    data = request.json

    data['last_update'] = dt.datetime.now()

    model = database.update_table_row('models', user_id, data)

    if not model:
        return jsonify({'error': 'Fallo en la actualización'}), 500

    return jsonify({'model': model.serialize()}), 200
