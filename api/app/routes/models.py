from flask import Blueprint, jsonify, request
import base64
import datetime as dt
from app.database import database
from app.models import Word 

models_bp = Blueprint('models', __name__, url_prefix='/models')

def get_file(file_id):
    try:
        file = database.read_by_id('models', file_id) 

        if file:
            # Codificar los datos binarios en Base64
            encoded_file_data = base64.b64encode(file.file_data).decode('utf-8')
            return file, encoded_file_data
        else:
            return None
    except Exception as e:
        print(f"Error retrieving the file: {e}")
        return None

@models_bp.route('/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    file = get_file(file_id)

    if file:
        file_obj, file_data = file 

        # Enviar la respuesta JSON con el archivo codificado
        return jsonify({
            'file': file_obj.serialize(),
            'file_data': file_data 
        }), 200
    else:
        return jsonify({"error": "File not found"}), 404

#CHECAR VERSION MODELO

@models_bp.route('/check_version/<int:user_id>', methods=['POST'])
def check_model_version(user_id):
    try:
        request_data = request.json
        request_date_str = request_data.get('date')        
        request_date = dt.strptime(request_date_str, "%d-%m-%Y %H:%M:%S")

        latest_model = database.read_by_field('models', 'id', user_id)
        if not latest_model:
            return jsonify({'error': 'No se encontró ningún modelo para este usuario.'}), 404

        latest_model_date = latest_model.last_update

        ####CLASS KEYS VERIFY
        # Verificación de class keys en la sesión
        session_class_keys = request_data.get("class_keys", {}).keys()
        
        # Obtener class keys desde la base de datos
        words = database.read_by_field('words', 'user_id', user_id)

        db_class_keys = [w.class_key for w in words]
        # Comparar class keys entre la sesión y la base de datos
        class_keys_faltantes = db_class_keys - session_class_keys
    
       # Comparar fechas
        is_updated = latest_model_date <= request_date  # True si está actualizado, False si hay una versión más nueva

        if is_updated and not class_keys_faltantes:
            return jsonify({
                'updated': True,
                'latest_version_date': latest_model_date.strftime('%Y-%m-%d %H:%M:%S'),
                'class_keys_status': 'sin_actualizacion'
            }), 200
        
        else:
            return jsonify({
                'updated': False,
                'latest_model': {
                    'id': latest_model.id,
                    'model_name': latest_model.model_name,
                    'latest_version_date': latest_model_date.strftime('%Y-%m-%d %H:%M:%S')
                },
                'palabras faltantes': [
            {
                'word': w.word,
                'class_key': w.class_key,
                'model': w.model
            }
            for w in words if w.class_key in class_keys_faltantes
        ],
                'class_keys_status': 'actualizacion_necesaria'
            }), 200

    except Exception as e:
        return jsonify({'error': f'Error al procesar la solicitud: {str(e)}'}), 500
    