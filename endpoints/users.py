from flask_restful import Resource
# from flask import request, Response
# from json import dumps

# from authenticate.auth import token_required
from databases.dbs import query_mysql
import json


def execute_request():
    sql_q = "SELECT * FROM Users"
    results_list = query_mysql(sql_q)
    # results_list = json.dumps(results_list)
    print(results_list)
    if len(results_list) == 0:
        return "User not found.", 400
    return results_list


class Users(Resource):
    @staticmethod
    # @token_required
    def get():
        return execute_request()


if __name__ == "__main__":
    execute_request()
