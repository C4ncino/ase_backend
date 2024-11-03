from datetime import datetime as dt
from app.database import database
from app.utils import pp_decorator
from flask import Blueprint, jsonify, request

models_bp = Blueprint('models', __name__, url_prefix='/models')


@models_bp.route('/check_version/<int:user_id>', methods=['POST'])
@pp_decorator(request, required_fields=['date', 'small'])
def check_model_version(user_id):
    try:
        request_data = request.json
        request_date_str = request_data.get('date')
        request_date = dt.strptime(request_date_str, "%d-%m-%Y %H:%M:%S")

        latest_model = database.read_by_id('models', user_id)

        if not latest_model:
            return jsonify(
                {'error': 'No se encontró ningún modelo para este usuario.'}
            ), 404

        latest_model_str = latest_model.last_update.strftime('%d-%m-%Y %H:%M:%S')

        latest_model_date = dt.strptime(latest_model_str, "%d-%m-%Y %H:%M:%S")

        session_class_keys = [int(key) for key in request_data.get("small", {}).keys()]

        words = database.read_by_field('words', 'user_id', user_id)

        db_class_keys = [w.class_key for w in words]

        class_keys_faltantes = set(db_class_keys) - set(session_class_keys)

        is_updated = latest_model_date == request_date

        has_missing_words = len(class_keys_faltantes) > 0

        return jsonify({
            'large_updated': is_updated,
            'latest_model': latest_model.serialize() if not is_updated else None,
            'small_updated': not has_missing_words,
            'small_models': [
                {
                    'word': w.word,
                    'class_key': w.class_key,
                    'model': w.model
                }
                for w in words if w.class_key in class_keys_faltantes
            ] if has_missing_words else None,
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
