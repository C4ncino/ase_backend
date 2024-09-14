from flask import Blueprint, jsonify
import base64
from app.database import database

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
