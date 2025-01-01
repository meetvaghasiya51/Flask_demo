from flask_restx import Namespace, Resource

# Define Namespace
main_ns = Namespace("Main", description="Main routes for the API")

@main_ns.route('/')
class Home(Resource):
    @main_ns.response(200, 'Welcome message retrieved successfully')
    def get(self):
        """
        Welcome endpoint for the Flask Demo API
        """
        return "Welcome to the Flask Demo API!", 200
