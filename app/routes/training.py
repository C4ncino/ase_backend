from flask import Blueprint, jsonify, request
from app.database import database
from flask_jwt_extended import jwt_required
import numpy as np

training_bp = Blueprint('training', __name__, url_prefix='/training')

@training_bp.route('/validate', methods=['POST'])
@jwt_required() 
def validate_training():

    data = request.json 

    try:
        # Obtener los datos de sensores del guante
        sensor_data = data.get('sensor_data')

        if not sensor_data or not isinstance(sensor_data, list) or len(sensor_data) < 15:
            return jsonify({'error': 'Se requieren al menos 15 lecturas'}), 400
        
        for sample in sensor_data:
            if len(sample) != 8:
                return jsonify({'error': 'Cada muestra debe contener exactamente 8 valores'}), 400

        max_variance_allowed = 5 
        inconsistent_count = 0


        # Verificar la coherencia en cada muestra
        for i in range(1, len(sensor_data)):
            current_sample = sensor_data[i]
            previous_sample = sensor_data[i - 1]

            # Calcular la varianza entre las muestras actuales y anteriores
            variance = np.var([current_sample, previous_sample], axis=0)

            # Verificación
            if any(variance > max_variance_allowed):
                inconsistent_count += 1
                
        if inconsistent_count > 0:
            return jsonify({
                'message': 'Se encontraron lecturas inconsistentes',
                'inconsistent_readings': inconsistent_count,
                'required_replacements': len(inconsistent_count)
            }), 400
        else:
            # Si los datos son coherentes, devolver una respuesta exitosa
            return jsonify({'message': 'Datos coherentes'}), 200

    except Exception as e:
        return jsonify({'error': f'Error al procesar los datos: {str(e)}'}), 500
