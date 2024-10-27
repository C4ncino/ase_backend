from flask import Blueprint, jsonify, request
# from flask_jwt_extended import jwt_required
from app.utils import pp_decorator
from app.database import database

# -----------------------------------------------------------------------------

words_bp = Blueprint('words', __name__, url_prefix='/words')

# -----------------------------------------------------------------------------


@words_bp.route('/<int:user_id>', methods=['GET'])
# @jwt_required()
def get_all_words(user_id):
    try:
        # Recuperar todas las palabras desde la base de datos
        words = database.read_by_field('words', 'user_id', user_id)

        # Agrupar las palabras en función de la primera letra
        sorted_words = sorted(words, key=lambda word: word.word.lower())

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

        return jsonify({'words': response_words}), 200

    except Exception as e:
        return jsonify(
            {'error': f'Error al procesar la solicitud: {str(e)}'}
        ), 500

@words_bp.route('/<int:word_id>', methods=['GET'])
# @jwt_required()
def get_word_model(word_id):
    try:
        word = database.read_by_id('words', word_id)

        if not word:
            return jsonify({'error': 'Palabra no encontrada'}), 404

        return jsonify({
            'word': word.word,
            'model': word.model,
            'class_key': word.class_key
        }), 200

    except Exception as e:
        return jsonify(
            {'error': f'Error al procesar la solicitud: {str(e)}'}
        ), 500


@words_bp.route('/<int:word_id>', methods=['PUT'])
# @jwt_required()
@pp_decorator(request, optional_fields=['word'])
def update_word(word_id):
    data = request.json

    try:
        existing_word = database.read_by_id('words', word_id)

        if not existing_word:
            return jsonify({'error': 'Palabra no encontrada'}), 404

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


@words_bp.route('/dump/<int:user_id>', methods=['GET'])
# @jwt_required()
def data_dump(user_id):
    try:
        words = database.read_by_field('words', 'user_id', user_id)

        if len(words) == 0:
            return jsonify(
                {'error': 'No se encontraron palabras para el usuario'}
            ), 404

        word_data_dump = []

        for word in words:

            word_data = database.read_by_id('data_words', word.id)

            word_info = word_data.serialize()

            word_data_dump.append(word_info)

        return jsonify({'dump': word_data_dump}), 200

    except Exception as e:
        return jsonify(
            {'error': f'Error al procesar la solicitud: {str(e)}'}
        ), 500


@words_bp.route('/exists/<int:user_id>/<string:word>', methods=['GET'])
# @jwt_required()
def check_word_exists(user_id, word):
    try:
        existing_words = database.read_by_fields('words', {'user_id': user_id, 'word': word.lower()})

        if existing_words:
            return jsonify({'exists': True, 'message': 'La palabra ya existe para este usuario'}), 200
        else:
            return jsonify({'exists': False, 'message': 'La palabra no existe para este usuario'}), 200

    except Exception as e:
        return jsonify({'error': f'Error al procesar la solicitud: {str(e)}'}), 500
    

@words_bp.route('/get/<int:word_id>', methods=['GET'])
# @jwt_required()
def get_word_by_id(word_id):
    try:
        word = database.read_by_id('words', word_id)

        if not word:
            return jsonify({'error': 'Palabra no encontrada'}), 404

        return jsonify({
            'word': word.word,
        }), 200

    except Exception as e:
        return jsonify({'error': f'Error al procesar la solicitud: {str(e)}'}), 500
