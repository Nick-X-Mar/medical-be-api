from flask import Flask
from flask_restful import Api
from endpoints.users import Users
from config import config


app = Flask(__name__)
api = Api(app)


api.add_resource(Users, '/members/update')


if __name__ == '__main__':
    app.run(debug=False, host=config.APP_ADDRESS, port=config.APP_PORT)
