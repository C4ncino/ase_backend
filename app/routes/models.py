from flask import Flask, jsonify
import base64
from app.database import DatabaseInterface, Model

app = Flask(__name__)

db_interface = DatabaseInterface()

def get_file(file_id):
    try:
        file = db_interface.read_by_id('models', file_id) 

        if file:
            # Codificar los datos binarios en Base64
            encoded_file_data = base64.b64encode(file.file_data).decode('utf-8')
            return file.filename, encoded_file_data
        else:
            return None
    except Exception as e:
        print(f"Error retrieving the file: {e}")
        return None

@app.route('/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    file = get_file(file_id)

    if file:
        filename, file_data = file 

        # Enviar la respuesta JSON con el archivo codificado
        return jsonify({
            'filename': filename,
            'file_data': file_data 
        }), 200
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
