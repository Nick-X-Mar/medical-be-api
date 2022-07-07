from flask_restful import Resource
from flask import request, Response
from json import dumps


def execute_request():
    pass


class Users(Resource):
    @staticmethod
    def get():
        return execute_request()
