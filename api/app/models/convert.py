import os
import json
import base64
import tempfile
import tensorflowjs as tfjs


def convert_model_to_tfjs(model):
    model_data = {}
    model_data['weights'] = {}

    with tempfile.TemporaryDirectory() as tmp_dir:
        output_dir = os.path.join(tmp_dir, 'tfjs_model')

        tfjs.converters.convert_keras_model(model, output_dir)

        json_file_path = os.path.join(output_dir, 'model.json')

        with open(json_file_path, 'r') as json_file:
            json_content = json.load(json_file)

            model_data['json'] = json_content

            weights_manifest = json_content['weightsManifest']

            for item in weights_manifest:
                paths = item["paths"]

                for path in paths:

                    long_path = os.path.join(output_dir, path)

                    with open(long_path, 'rb') as bin_file:
                        data = base64.b64encode(bin_file.read())

                        string_data = data.decode('utf-8')

                        model_data['weights'][path] = string_data

    return model_data
