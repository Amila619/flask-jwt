from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)


@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user_data():
    # Extract the data from the JWT
    user = get_jwt_identity()

    if user:
        return user
    else:
        return {'message': 'User not found'}, 404


