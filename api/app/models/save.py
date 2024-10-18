import os
import tempfile
import tensorflowjs as tfjs


def save_model_as_tensorflowjs(model):
    model_data = None

    # Crear un directorio temporal para guardar el modelo convertido
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Convertir el modelo keras a formato TensorFlow.js y guardarlo en el directorio temporal
        tfjs_output_dir = os.path.join(tmp_dir, 'tfjs_model')
        tfjs.converters.convert_keras_model(model, tfjs_output_dir)
        
        # Buscar el archivo model.json generado
        json_file_path = os.path.join(tfjs_output_dir, 'model.json')
        with open(json_file_path, 'r') as json_file:
            json_content = json_file.read()

            model_data = json_content

    return model_data
