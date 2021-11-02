# in-built imports
from datetime import datetime, timedelta

# third party imports
import jwt
from flask import jsonify
from jwt import InvalidTokenError

# local imports
from app import db
from config import Config


class AuthService:
    def sign_in(self, auth_info: dict, model: db.Model):
        if not auth_info or not auth_info.get("username") or not auth_info.get("password"):
            return jsonify({
                "status": "error",
                "error": "authentication information required"
            })
        user = model.query.filter_by(
            username=auth_info.get("username")).first()
        if user:
            if not user.verification_status:
                return jsonify({
                    "status": "error",
                    "error": "account unverified"
                })
            if user.verify_password(auth_info.get("password")):
                user_token = self.create_token(user.id)
                return jsonify({
                    "access_token": user_token[0],
                    "refresh_token": user_token[1]
                })
        return jsonify({
            "status": "error",
            "error": "user verification failure. invalid credentials"
        })

    def create_token(self, id: int):
        payload = {
            'id': id,
            'exp': datetime.utcnow() + timedelta(days=1),
            'grant_type': 'access_token'
        }
        access_token = jwt.encode(
            payload, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM
        )
        payload["grant_type"] = "refresh_token"
        payload["exp"] = datetime.utcnow() + timedelta(days=1)
        refresh_token = jwt.encode(
            payload, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM
        )
        return [access_token, refresh_token]

    def decode_token(self, token: str):
        try:
            decode_token = jwt.decode(
                token, Config.SECRET_KEY, algorithms=Config.JWT_ALGORITHM
            )
        except InvalidTokenError as invalid_token:
            return invalid_token.args
        return decode_token
