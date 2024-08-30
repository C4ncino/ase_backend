"""
Define user routes
"""
from app.utils import pp_decorator
from flask import Blueprint, jsonify, request
# TODO: For db use uncomment this
# from app.database import database

example_bp = Blueprint('example_routes', __name__, url_prefix="/users")


@example_bp.route("/")
def home():
    return "Hello World"


@example_bp.route("/", methods=['POST'])
@pp_decorator(request, required_fields=['name'])
def ppExample():
    data = request.json

    return jsonify(data), 200


# TODO: For db example uncomment the two methods
# @example_bp.route( + 'example', methods=['POST'])
# @pp_decorator(request, required_fields=['name'])
# def createRow():
#     _, row = database.create_table_row('examples', request.json)

#     return jsonify(row.serialize()), 200


# @example_bp.route( + 'example/<id>', methods=['PUT'])
# @pp_decorator(request, optional_fields=['name'])
# def updateRow(id):
#     row = database.update_table_row('examples', id, request.json)

#     return jsonify(row.serialize()), 200
