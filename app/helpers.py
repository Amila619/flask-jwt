from .database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from flask_jwt_extended import decode_token
from flask import current_app as app
from .models import Token

def add_token_to_database(access_token):

    db : Session = get_db()

    decoded_token = decode_token(access_token)

    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_id = decoded_token['sub']['id']
    expires = datetime.fromtimestamp(decoded_token['exp'])

    db_token = Token(
        jti=jti,
        token_type=token_type,
        user_id=user_id,
        expires=expires
    )
    
    db.add(db_token)
    db.commit()
    db.refresh(db_token)


def revoke_token(token_jti, user_id):

    db : Session = get_db()

    try:
        token = db.query(Token).filter_by(jti=token_jti, user_id=user_id).update({Token.revoked_at: datetime.utcnow()}, synchronize_session=False)
        db.commit()
    except NoResultFound:
        raise Exception(f"Could not find token {token_jti}")
    

def is_token_revoked(jwt_payload):

    db : Session = get_db()

    token_jti = jwt_payload['jti']
    user_id = jwt_payload['sub']['id']

    try:
        token = db.query(Token).filter_by(jti=token_jti, user_id=user_id).first()
        return token.revoked_at is not None
    except NoResultFound:
        raise Exception(f"Could not find token {token_jti}")
    