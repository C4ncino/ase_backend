"""
Define user routes
"""


from flask_jwt_extended import create_access_token
from flask import Blueprint, jsonify, request, make_response
from app.utils import pp_decorator
from app.database import database
from app.database import User 


users_bp = Blueprint('example_routes', __name__, url_prefix='/users')

@users_bp.route('/login', methods=['POST'])
@pp_decorator(request, required_fields=['email', 'password']) 
def login():
    #obtiene JSOn enviados en la solicitud
    data = request.json 
    email = data.get('email')
    password = data.get('password')

    #busca el email en la base de datos
    result = database.read_by_fields(
        'users', 
        [
            {
                "field": "email",
                "value": email,
                "comparison": "eq"
            },{
                "field": "password",
                "value": password,
                "comparison": "eq"
            }
        ]
    )

    #contraseña o email incorrecto
    if len(result) == 0 or len(result) > 1:
        return jsonify({'error': 'Credenciales inválidas'}), 401

    #generan token JWT
    token = create_access_token( {'email': email} )

    # devolver token
    return jsonify(
        {
            'user': result[0].serialize(),
            'token': token
        }
    ), 200


@users_bp.route('/sign-up', methods=['POST'])
@pp_decorator(request, required_fields=['email', 'password', 'name', 'last_name', 'bday', 'password']) 

def signup():
    data = request.json

    try:
        success, user = database.create_table_row('users', data)
        
        if not success:
            return make_response(jsonify({'error': 'Fallo en el registro'}), 500)
        
        token = create_access_token({'email': user.email})

        return jsonify(
            {
                'user': user.serialize(),
                'token': token
            }
        ), 201

    except:
        return jsonify({'error': 'Correo ya registrado'}), 400


