from flask import Blueprint

# Create a blueprint for the routes
main = Blueprint('main', __name__)

# Import route handlers
from . import example_routes  # Assuming you will create example_routes.py for handling specific routes
from . import transcribe_routes