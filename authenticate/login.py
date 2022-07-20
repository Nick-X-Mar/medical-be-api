from flask import Flask, request, jsonify, make_response
from config import config
from datetime import datetime, timedelta
from endpoints.email import execute_request
import jwt
from flask_restful import Resource


JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 60


def execute_login(email, password):
    user_data, status = execute_request(email=email)
    if status == 200:
        if user_data.get('password') != password:
            return {'message': 'Wrong credentials'}, 400

        payload = {
            'user_id': user_data.get('id'),
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        return {'token': jwt_token}, 200
    else:
        return {"msg": user_data, "status": status}


def check_request(email, password):
    if email is None and email == "":
        return 400, "Email was not given."

    if password is None and password == "":
        return 400, "Password was not given."

    return 200, ""


class Auth(Resource):
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



# def login():
#     # creates dictionary of form data
#     auth = request.form
#
#     if not auth or not auth.get('email') or not auth.get('password'):
#         # returns 401 if any email or / and password is missing
#         return make_response(
#             'Could not verify',
#             401,
#             {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
#         )
#
#     user = User.query \
#         .filter_by(email=auth.get('email')) \
#         .first()
#
#     if not user:
#         # returns 401 if user does not exist
#         return make_response(
#             'Could not verify',
#             401,
#             {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
#         )
#
#     if check_password_hash(user.password, auth.get('password')):
#         # generates the JWT Token
#         token = jwt.encode({
#             'public_id': user.public_id,
#             'exp': datetime.utcnow() + timedelta(minutes=30)
#         }, app.config['SECRET_KEY'])
#
#         return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
#     # returns 403 if password is wrong
#     return make_response(
#         'Could not verify',
#         403,
#         {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
#     )
#
#
# # signup route
# @app.route('/signup', methods=['POST'])
# def signup():
#     # creates a dictionary of the form data
#     data = request.form
#
#     # gets name, email and password
#     name, email = data.get('name'), data.get('email')
#     password = data.get('password')
#
#     # checking for existing user
#     user = User.query \
#         .filter_by(email=email) \
#         .first()
#     if not user:
#         # database ORM object
#         user = User(
#             public_id=str(uuid.uuid4()),
#             name=name,
#             email=email,
#             password=generate_password_hash(password)
#         )
#         # insert user
#         db.session.add(user)
#         db.session.commit()
#
#         return make_response('Successfully registered.', 201)
#     else:
#         # returns 202 if user already exists
#         return make_response('User already exists. Please Log in.', 202)