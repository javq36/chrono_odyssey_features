from flask import Flask
from flask_cors import CORS
from routes.transcribe_routes import transcribe_bp
from routes.summarize_routes import summarize_bp
from routes.reddit_scraper_routes import reddit_scraper_bp
from services import db_service # Import the db_service module

from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Initialize the database
    db_service.init_db() 
    print("Database initialized from app.py") # Optional: for confirmation

    app.register_blueprint(transcribe_bp)
    app.register_blueprint(summarize_bp)
    app.register_blueprint(reddit_scraper_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)