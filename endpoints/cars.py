from flask_restful import Resource
from flask import request, make_response
from authenticate.auth import token_required
from databases.dbs import query_mysql


def get_user_by_id(member_id):
    sql_q = f"SELECT * FROM Users WHERE Users.id = {member_id};"
    data, status = query_mysql(sql_q)
    # results_list = json.dumps(results_list)
    print(data)
    if len(data) == 0:
        return {"message": "User not found."}, 404
    return data[0], 200


def execute_get_user_by_email(email):
    sql_q = f"SELECT * FROM Users WHERE Users.email = '{email}';"
    data, status = query_mysql(sql_q)
    # results_list = json.dumps(results_list)
    print(data)
    if len(data) == 0:
        return "User not found.", 404
    elif len(data) > 1:
        msg = f"Error: Found {len(data)} users with: {email} as their email."
        return msg, 400
    return data[0], 200


def get_all_users():
    sql_q = "SELECT * FROM Users"
    results_list = query_mysql(sql_q)
    # results_list = json.dumps(results_list)
    print(results_list)
    if len(results_list) == 0:
        return {"message": "User not found."}, 400
    return results_list[0], 200


def register_new_car(args):
    model = args.get('model')
    brand = args.get('brand')
    year = args.get('year')
    khm = args.get('khm')
    cc = args.get('cc')
    hp = args.get('hp')
    # generate_password_hash(password)
    # check_password_hash(user.password, auth.get('password')
    # Todo: get buy email for check already exists
    user, status = execute_get_user_by_email(email)
    if status != 404 and user != "User not found.":
        return make_response("User already exists. Please Log in.", 200)
    sql_q = f"""insert INTO Users (title, firstName, lastName, email, role, password, dateCreated, dateUpdated)
            VALUES ( '{title}', '{firstName}', '{lastName}', '{email}', '{role}', '{password}', now(), now());"""
    print(sql_q)
    msg, status = query_mysql(sql_q)
    if status == 200:
        return {"message": "User Registered"}, status
    else:
        return {"message": msg}, status


def delete_user(args):
    member_id = args.get('member_id')
    user, status = get_user_by_id(member_id)
    if status == 404 and user == "User not found.":
        return {'message':  "User not found."}, 404
    sql_q = f"""DELETE FROM `Users` WHERE Users.id = {member_id};"""
    print(sql_q)
    msg, status = query_mysql(sql_q)
    if status == 200:
        return {'message':  "User Delete."}, 200
    else:
        return {'message':  msg}, status


def update_user(args, body):
    member_id = args.get('member_id')
    title = body.get('title')
    firstName = body.get('firstName')
    lastName = body.get('lastName')
    role = body.get('role')
    email = body.get('email')
    password = body.get('password')

    user, status = get_user_by_id(member_id)
    if status == 404 and user == "User not found.":
        return {'message': "User not found."}, 404
    sql_q = f"""UPDATE Users set title = '{title}', firstName = '{firstName}', lastName = '{lastName}', role = '{role}', email = '{email}', password = '{password}' WHERE Users.id = {member_id};"""
    print(sql_q)
    msg, status = query_mysql(sql_q)
    if status == 200:
        return {'message': "User Updated."}, 200
    else:
        return {'message': msg}, status


def check_request_post(args):
    model = args.get('model')
    brand = args.get('brand')
    year = args.get('year')
    khm = args.get('khm')
    cc = args.get('cc')
    hp = args.get('hp')

    if any(item is None for item in [model, brand, year, khm, cc, hp]):
        return {'message': 'Please complete all required fields.'}, 400

    return "", 200


def check_request_delete(args):
    member_id = args.get('member_id')
    if member_id is None and member_id == "":
        return {"message": "member_id was not given."}, 400
    return "", 200


def check_request_put(args, body):
    if body is None:
        return {'message': 'Nothing send for update'}, 400

    member_id = args.get('member_id')
    if member_id is None and member_id == "":
        return {"message": "member_id was not given."}, 400

    title = body.get('title')
    firstName = body.get('firstName')
    lastName = body.get('lastName')
    role = body.get('role')
    email = body.get('email')
    password = body.get('password')

    # if email is None or email == "":
    #     return {"message": "Email was not given."}, 400

    if any(item is None for item in [title, firstName, lastName, email, role, password]):
        return {'message': 'Please complete all required fields.'}, 400

    return "", 200


class Cars(Resource):

    # Get All Users
    @staticmethod
    # @token_required
    def get():
        email = request.args.get('email')
        if email is not None and email != "":
            exe_msg, exe_status = execute_get_user_by_email(email)
            if exe_status == 200:
                return {"user": exe_msg}, exe_status
            else:
                return {"message": exe_msg}, exe_status

        member_id = request.args.get('member_id')
        if member_id is not None and member_id != "":
            msg, status = get_user_by_id(member_id)
            if status == 200:
                return {"user": msg}, status
            else:
                return {"message": msg}, status

        msg, status = get_all_users()
        if status == 200:
            return {"users": msg}, status
        else:
            return {"message": msg}, status

    # Add Car
    @staticmethod
    def post():
        body = request.json
        msg, status = check_request_post(body)
        if status == 200:
            return register_new_car(body)
        else:
            return msg, status

    @staticmethod
    # @token_required
    def delete():
        args = request.args
        msg, status = check_request_delete(args)
        if status == 200:
            return delete_user(args)
        else:
            return msg, status

    # Update Users
    @staticmethod
    # @token_required
    def put():
        args = request.args
        body = request.json
        msg, status = check_request_put(args, body)
        if status == 200:
            return update_user(args, body)
        else:
            return msg, status
