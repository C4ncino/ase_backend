"""
Define user routes
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.utils import pp_decorator
from app.database import database


users_bp = Blueprint('example_routes', __name__, url_prefix='/users')


@users_bp.route('/login', methods=['POST'])
@pp_decorator(request, required_fields=['email', 'password'])
def login():
    # obtiene JSOn enviados en la solicitud
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # busca el email en la base de datos
    result = database.read_by_fields(
        'users',
        [
            {
                "field": "email",
                "value": email,
                "comparison": "eq"
            },
            {
                "field": "password",
                "value": password,
                "comparison": "eq"
            }
        ]
    )

    # contraseña o email incorrecto
    if len(result) == 0 or len(result) > 1:
        return jsonify({'error': 'Credenciales inválidas'}), 401

    user_id = result[0].id

    # generan token JWT
    token = create_access_token(
        {
            'user_id': user_id,
            'email': email
        },
        fresh=True
    )

    # devolver token
    return jsonify(
        {
            'user': result[0].serialize(),
            'token': token,
        }
    ), 200


@users_bp.route('/sign-up', methods=['POST'])
@pp_decorator(
    request,
    required_fields=[
        'email', 'password', 'name',
        'last_name', 'bday'
    ]
)
def signup():
    data = request.json

    try:
        success, user = database.create_table_row('users', data)

        if not success:
            return jsonify({'error': 'Fallo en el registro'}), 500

        token = create_access_token({'user_id': user.id, 'email': user.email})

        return jsonify(
            {
                'user': user.serialize(),
                'token': token
            }
        ), 201

    except Exception:
        return jsonify({'error': 'Correo ya registrado'}), 400


@users_bp.route('/refresh')
@jwt_required()
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(current_user)

    return jsonify({'token': new_access_token}), 200


@users_bp.route('/me')
@jwt_required()
def me():
    # Obtener el ID de usuario encriptado desde el token
    current_user = get_jwt_identity()
    user_id = current_user.get('user_id')

    # Buscar el usuario en la base de datos usando el ID
    user = database.read_by_id('users', user_id)

    if user is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify({'user': user.serialize()}), 200


@users_bp.route('/update', methods=['PUT'])
@pp_decorator(request, optional_fields=['name', 'last_name', 'bday'])
@jwt_required()
def update():
    data = request.json

    user_id = get_jwt_identity().get('user_id')

    success, user = database.update_table_row('users', user_id, data)

    if not success:
        return jsonify({'error': 'Fallo en la actualización'}), 500

    return jsonify({'user': user.serialize()}), 200
