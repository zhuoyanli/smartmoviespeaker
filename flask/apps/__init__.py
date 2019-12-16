from apps.api import bp as api_bp
from flask import Flask

def create_api():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix='/api')
    return app
