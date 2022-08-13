from flask import Flask
from flask_restful import Api

from authenticate.login import Login
from endpoints.delete import DeleteUser
from endpoints.update import UpdateUser
from endpoints.users import Users
from endpoints.email import Email
from config import config


app = Flask(__name__)
# app.config['SECRET_KEY'] = config.SECRET_KEY
api = Api(app)

root = "/medical"

api.add_resource(Login,  root + '/login', endpoint='login', methods=['POST'])

# Get All Users
api.add_resource(Users, root + '/users', endpoint='get_all_users', methods=['GET'])

# Add New User
api.add_resource(Users, root + '/users/signup', endpoint='signup_user', methods=['POST'])

# Edit User
api.add_resource(Users, root + '/users/edit', endpoint='edit_user', methods=['PUT'])

# Delete User
api.add_resource(Users, root + '/users/delete', endpoint='delete_user', methods=['DELETE'])

# Get single User by Email
api.add_resource(Users, root + '/users/email', endpoint='get_user_by_email', methods=['GET'])

# Get single User by Id
api.add_resource(Users, root + '/users/member_id', endpoint='get_user_by_id', methods=['GET'])

if __name__ == '__main__':
    print(f"Host:{config.APP_ADDRESS}, \nPort:{config.APP_PORT}")
    app.run(debug=False, host=config.APP_ADDRESS, port=config.APP_PORT)
