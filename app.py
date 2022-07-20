from flask import Flask
from flask_restful import Api

from authenticate.login import Auth
from endpoints.users import Users
from endpoints.email import Email
from config import config


app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
api = Api(app)

root = "/medical"

api.add_resource(Auth,  root + '/login')

api.add_resource(Users, root + '/users')
api.add_resource(Email, root + '/users/email')

if __name__ == '__main__':
    print(f"Host:{config.APP_ADDRESS}, \nPort:{config.APP_PORT}")
    app.run(debug=False, host=config.APP_ADDRESS, port=config.APP_PORT)
