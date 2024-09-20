from flask import Flask
from app.webhooks.routes import app_bp
from flask_cors import CORS
from app.extensions import init_mongo

def create_app():

    app = Flask(__name__)

    CORS(app)  #handling cross platform

    app.config["MONGO_URI"] = "mongodb://localhost:27017/events" #mongodb URI
    init_mongo(app = app)


    app.register_blueprint(app_bp)

    return app