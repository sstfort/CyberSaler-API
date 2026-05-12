from utils.getenv import getenv

from flask import Flask, jsonify, request, g
from flask_smorest import Api
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request, get_jwt, decode_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

from flask_compress import Compress

from datetime import timedelta

from db import db
from blocklist import BLOCKLIST
import json
import requests

from ressources.entreprise import blp as EntrepriseBluePrint
from ressources.distribution import blp as DistributionBluePrint
from ressources.categorie import blp as CategorieBluePrint
from ressources.article import blp as ArticleBluePrint
from ressources.achat import blp as AchatBluePrint
from ressources.prix_vente import blp as PrixVenteBluePrint
from ressources.vente import blp as VenteBluePrint
from ressources.user import blp as UserBluePrint
from ressources.level import blp as LevelBluePrint
from ressources.vente_complet import blp as VenteCompletBluePrint



        

def create_app(db_url=None):
    app = Flask(__name__)

    Compress(app)


    @app.after_request
    def add_header(response):
        response.headers["X-Server"] = "Server-D"  # 👈 For 185.246.86.187  
        return response

    # Load database configuration
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "CyberSaler REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" 
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv()["DATABASE_URL"]
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 280}
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    # app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

    # initialize JWT
    app.config["JWT_SECRET_KEY"] = getenv()["JWT_SECRET_KEY"]
    jwt = JWTManager(app)

    
    api = Api(app)
    db.init_app(app)


    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )


    
    
    @app.before_request
    def create_all():
        db.create_all()


    api.register_blueprint(EntrepriseBluePrint)
    api.register_blueprint(DistributionBluePrint)
    api.register_blueprint(CategorieBluePrint)
    api.register_blueprint(ArticleBluePrint)
    api.register_blueprint(AchatBluePrint)
    api.register_blueprint(PrixVenteBluePrint)
    api.register_blueprint(VenteBluePrint)
    api.register_blueprint(UserBluePrint)
    api.register_blueprint(LevelBluePrint)
    api.register_blueprint(VenteCompletBluePrint)

    @app.after_request
    def call(response):
        #print("Current DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])
        return response  # 🔥 Important: Must return response

    return app

    

app = create_app()
