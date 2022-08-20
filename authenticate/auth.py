import jwt
# from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, make_response
from config import config


# decorator for verifying the JWT
from endpoints import users


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return {'message': 'Token is missing !!'}, 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
            user, status = users.execute_get_user_by_email(data.get('email'))
            if status == 404 and user == "User not found.":
                return {'message': "User not Found."}, 200
        except:
            return {'message': 'Token is invalid !!'}, 401
        # returns the current logged in users contex to the routes
        return f(*args, **kwargs)

    return decorated
