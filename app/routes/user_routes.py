from flask_jwt_extended import jwt_required
from flask_restx import Namespace, fields, Resource
from app.models import User

user_ns = Namespace("User", description="User operations for items")

user_model = user_ns.model(
    'User',
    {
        'email': fields.String(required=True, description='User email'),
        'password': fields.String(required=True, description='User password'),
    }
)

@user_ns.route('/')
class UserList(Resource):
    @user_ns.response(200, 'Success')
    @jwt_required()
    def get(self):
        """
        Get all users
        """
        users = User.query.all()
        print('users :: ', users)
        return [{'id': user.id, 'email': user.email, 'password': user.password} for user in users], 200

    # @user_ns.expect(user_model, validate=True)
    # @user_ns.response(201, 'User created successfully')
    # @user_ns.response(400, 'Invalid input')
    # @jwt_required()
    # def post(self):
    #     """
    #     Create a new user
    #     """
    #     data = request.get_json()
    #     user = User(email=data['email'], password=data['password'])
    #     db.session.add(user)
    #     db.session.commit()
    #     return {'message': 'User created successfully'}, 201
