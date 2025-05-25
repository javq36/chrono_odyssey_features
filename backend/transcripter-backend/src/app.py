from flask import Flask
from flask_cors import CORS
from routes.transcribe_routes import transcribe_bp
from routes.summarize_routes import summarize_bp
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.register_blueprint(transcribe_bp)
    app.register_blueprint(summarize_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)