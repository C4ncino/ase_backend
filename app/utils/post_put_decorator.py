""""
Decorator to validate if the fields are in a POST or PUT request
"""
from flask import Request, jsonify


def validate(request: Request, fields: list[str]) -> str:
    """
    Validate if the fields are in the request

    Args:
        request: The request
        fields: The fields to validate

    Returns:
        A str with The errors
    """

    possible_errors = {}

    for field in fields:
        if field not in request.json:
            possible_errors[field] = f"'{field}' is needed"

    if request.method == 'POST':
        return possible_errors, len(possible_errors) == 0

    if request.method == 'PUT':
        error_msg = "At least one field is required of the following: "
        error_msg += ', '.join(fields)
        return error_msg, len(possible_errors) < len(fields)

    return None


def pp_decorator(
    request: Request,
    required_fields: list[str] | None = None,
    optional_fields: list[str] | None = None
):
    """
    Decorator to validate if the fields are in the request

    Args:
        request: The request
        required_fields: The fields to validate
        optional_fields: The fields to validate

    Returns:
        str: The errors
    """

    if required_fields is None:
        required_fields = []

    if optional_fields is None:
        optional_fields = []

    def decorador(func):

        wrapper_name = f"{func.__name__}_wrapper"

        def wrapper(*args, **kwargs):
            if request.method in ('POST', 'PUT'):
                if not request.json:
                    return jsonify({
                        "message": "A body in JSON format is needed"
                    }), 400

                errors, validated = validate(
                    request,
                    required_fields if request.method == 'POST'
                    else optional_fields
                )

                if not validated:
                    return jsonify(
                        {"message": errors} if request.method == 'PUT'
                        else {
                            "message": "Fields are missing",
                            "errors": errors
                        }
                    ), 400

            return func(*args, **kwargs)

        wrapper.__name__ = wrapper_name

        return wrapper

    return decorador
