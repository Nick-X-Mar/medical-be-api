import json
from flask_restful import Resource
from flask import request, Response, jsonify
# from authenticate.auth import token_required
from databases.dbs import query_mysql


def execute_request(email):
    sql_q = f"SELECT * FROM Users WHERE Users.email = '{email}';"
    results_list = query_mysql(sql_q)
    # results_list = json.dumps(results_list)
    print(results_list)
    if len(results_list) == 0:
        return "User not found.", 400
    elif len(results_list) > 1:
        msg = f"Error: Found {len(results_list)} users with: {email} as their email."
        return msg, 400
    return results_list[0], 200


def check_request():
    email = request.args.get('email')
    if email is not None and email != "":
        return 200, ""
    return 400, "Email was not given."


class Email(Resource):
    @staticmethod
    # @token_required
    def get():
        email = request.args.get('email')
        status, msg = check_request()
        if status == 200:
            return execute_request(email)
        else:
            return jsonify({msg}), status


if __name__ == "__main__":
    execute_request('ym2000gr@yahoo.com')
