from flask import Blueprint, jsonify, request
from app.database import database
from app.utils import pp_decorator
from flask_jwt_extended import jwt_required
import numpy as np

training_bp = Blueprint('training', __name__, url_prefix='/training')

@training_bp.route('/validate', methods=['POST'])
@jwt_required()
@pp_decorator(request, required_fields=['sensor_data', 'user_id']) 
def validate_training():

    data = request.json 

    # Datos sensor
    sensor_data = data.get('sensor_data')

    #Checa que sea una lista
    if not sensor_data or not isinstance(sensor_data, list):
        return jsonify({'error': 'sensor_data debe ser una lista'}), 400
    
    #Checa que sean 18 lecturas
    if len(sensor_data) < 18:
        return jsonify({'error': 'Se requieren al menos 18 lecturas en sensor_data'}), 400
    
    #Checa que sea  60x8
    for matrix in sensor_data:
        if len(matrix) != 60 or len(matrix[0]) != 8:
            return jsonify({'error': 'Cada matriz debe contener 60 filas y 8 columnas'}), 400

    max_variance_allowed = 0.6
    inconsistent_matrices = []

    #Convierte los datos del sensor en arreglo
    sensor_data_np = np.array(sensor_data)

    #Flex son los primeros 5
    #Acc inicia en el 6
    flex_data_np = sensor_data_np[:, :5]
    accelerometer_data_np = sensor_data_np[:, 5:]

    # Compara las matrices (60x8) para flex y acelerómetro por separado
    for i in range(len(sensor_data_np)):
        current_flex_matrix = flex_data_np[i]

        for j in range(i + 1, len(sensor_data_np)):
            other_flex_matrix = flex_data_np[j]
    
            flex_variance = np.var([current_flex_matrix, other_flex_matrix], axis=0)
            if np.any(flex_variance > max_variance_allowed):
                pass
        
