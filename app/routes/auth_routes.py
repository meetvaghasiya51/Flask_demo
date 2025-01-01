from datetime import datetime
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from .. import db, bcrypt
from ..models import User
from flask_jwt_extended import create_access_token

# Define Namespace
auth_ns = Namespace("Auth", description="Authentication APIs")

# Define Request Models for Swagger
register_model = auth_ns.model(
    'Register', 
    {
        'email': fields.String(required=True, description='User email'),
        'password': fields.String(required=True, description='User password')
    }
)

login_model = auth_ns.model(
    'Login', 
    {
        'email': fields.String(required=True, description='User email'),
        'password': fields.String(required=True, description='User password')
    }
)

# Define API Routes with Swagger Documentation
@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model, validate=True)
    @auth_ns.response(201, 'User registered successfully')
    @auth_ns.response(400, 'Invalid input')
    def post(self):
        """
        Register a new user
        """
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(email=data['email'], password=hashed_password, created_at=datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, 'Login successful')
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """
        Authenticate a user and return an access token
        """
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.email)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401
