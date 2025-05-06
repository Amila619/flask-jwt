from flask import Blueprint, request
from pydantic import ValidationError
from .database import engine, get_db
from sqlalchemy.orm import Session
from flask_jwt_extended import create_access_token, create_refresh_token, JWTManager, jwt_required, get_jwt_identity, get_jwt
from .helpers import add_token_to_database, is_token_revoked, revoke_token
from . import schemas, models

auth_bp = Blueprint('auth', __name__)

jwt = JWTManager()

@auth_bp.route('/register', methods=["POST"])
def register_user():
    db : Session = get_db()

    try:
        data = request.get_json()
        user = schemas.UserCreate(**data)
    except ValidationError as e:
        return e.errors()[0], 400

    user_ = db.query(models.User).filter(models.User.email == data['email']).first()
    if user_:
        return {"message" : "user already registered"}, 403

    new_user = models.User(**user.dict())
    new_user.set_password(new_user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return_new_user = schemas.UserResponse(**new_user.as_dict())
    return return_new_user.dict(), 201

@auth_bp.route('/login', methods=["POST"])
def login_user():
    db : Session = get_db()
    
    try:
        data = request.get_json()
        user = schemas.UserLogin(**data)
    except ValidationError as e:
        return e.errors()[0], 400

    user_ = db.query(models.User).filter(models.User.email == data['email']).first()

    if user_ and user_.check_password(data['password']):
        return_user = schemas.UserResponse(**user_.as_dict())
        access_token = create_access_token(identity=return_user.dict())
        refresh_token = create_refresh_token(identity=return_user.dict())

        add_token_to_database(access_token)
        add_token_to_database(refresh_token)
        
        return {'message': 'Login Success', 'access_token': access_token, 'refresh_token': refresh_token,}
    
    return {'message': 'Login Failed'}, 401

@auth_bp.route('/refresh', methods=["POST"])
@jwt_required(refresh=True)
def referesh_token():
    # Extract the data from the JWT
    user = get_jwt_identity()

    access_token = create_access_token(identity=user)
    add_token_to_database(access_token)

    return {'access_token': access_token}
    

@auth_bp.route('/revoke_access', methods=['DELETE'])
@jwt_required()
def revoke_access_token():
    jti = get_jwt()['jti']
    user_id = get_jwt_identity()['id']
    revoke_token(jti, user_id)
    return {"msg" : "Token revoked"}, 200

@auth_bp.route('/revoke_refresh', methods=['DELETE'])
@jwt_required(refresh=True)
def revoke_refresh_token():
    jti = get_jwt()['jti']
    user_id = get_jwt_identity()['id']
    revoke_token(jti, user_id)
    return {"msg" : "Refresh Token revoked"}, 200

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    try:
        return is_token_revoked(jwt_payload)
    except Exception:
        return True








