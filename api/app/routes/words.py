"""
Define words routes
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils import pp_decorator
from app.database import database

# -----------------------------------------------------------------------------

words_bp = Blueprint('words', __name__, url_prefix='/words')

# -----------------------------------------------------------------------------


# ADD WORD
@words_bp.route('', methods=['POST'])
# @jwt_required()
@pp_decorator(request, required_fields=['word', 'sensor_data', 'user_id'])
def add_word():
    # Obtener datos de la solicitud
    data = request.json

    try:
        success, word_entry = database.create_table_row('words', data)

        if not success:
            return jsonify({'error': 'Error al registrar la palabra'}), 500

        return jsonify(
            {
                'message': 'Palabra registrada exitosamente',
                'word': word_entry.serialize()
            }), 201

    except Exception as e:
        return jsonify(
            {'error': f'Error al procesar la solicitud: {str(e)}'}
        ), 500


# GET ALL
@words_bp.route('/<int:user_id>', methods=['GET'])
# @jwt_required()
def get_all_words(user_id):
    try:
        # Recuperar todas las palabras desde la base de datos
        words = database.read_by_field('words', 'user_id', user_id)
        sorted_words = sorted(words, key=lambda word: word.word.lower())
        # Agrupar las palabras en función de la primera letra

        grouped_words = {}

        for word in sorted_words:
            first_letter = word.word[0].upper()
            group_key = f'{first_letter}{first_letter.lower()}'
            if group_key not in grouped_words:
                grouped_words[group_key] = []
            grouped_words[group_key].append(word.serialize())

        response_words = []
        for key, value in grouped_words.items():
            response_words.append({
                "title": key,
                "data": value
            })

        # Serializar cada palabra antes de devolverla
        return jsonify({'words': response_words}), 200

    except Exception as e:
        return jsonify(
            {'error': f'Error al procesar la solicitud: {str(e)}'}
        ), 500


# UPDATE
@words_bp.route('/<int:word_id>', methods=['PUT'])
# @jwt_required()
@pp_decorator(request, optional_fields=['word'])
def update_word(word_id):
    data = request.json

    try:
        # Verificar si la palabra existe
        existing_word = database.read_by_id('words', word_id)

        if not existing_word:
            return jsonify({'error': 'Palabra no encontrada'}), 404

        # Actualizar la palabra
        updated_data = {
            'word': data['word']
        }

        updated_word = database.update_table_row(
            'words', word_id, updated_data
        )

        return jsonify(
            {
                'message': 'Palabra actualizada exitosamente',
                'word': updated_word.serialize()
            }
        ), 200

    except Exception as e:
        return jsonify(
            {'error': f'Error al procesar la solicitud: {str(e)}'}
        ), 500
