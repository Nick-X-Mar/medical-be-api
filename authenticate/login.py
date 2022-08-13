from flask import Flask, request, jsonify, make_response
from config import config
from datetime import datetime, timedelta
from endpoints.email import execute_get_user_by_email
import jwt
from flask_restful import Resource


# JWT_SECRET = 'secret'
# JWT_ALGORITHM = 'HS256'
# JWT_EXP_DELTA_SECONDS = 60


def execute_login(email, password):
    user_data, status = execute_get_user_by_email(email=email)
    if status == 200:
        if user_data.get('password') != password:
            return {'message': 'Wrong credentials'}, 400

        payload = {
            'user_id': user_data.get('id'),
            'email': email,
            'exp': datetime.utcnow() + timedelta(seconds=config.JWT_EXP_DELTA_SECONDS)
        }
        jwt_token = jwt.encode(payload, config.JWT_SECRET, config.JWT_ALGORITHM)
        return {'token': jwt_token}, 200
    else:
        return {"msg": user_data, "status": status}


def check_request(email, password):
    if email is None and email == "":
        return 400, "Email was not given."

    if password is None and password == "":
        return 400, "Password was not given."

    return 200, ""


class Login(Resource):
    @staticmethod
    # @token_required
    def post():
        email = request.args.get('email')
        password = request.args.get('password')
        status, msg = check_request(email, password)
        if status == 200:
            return execute_login(email, password)
        else:
            return jsonify({msg}), status
