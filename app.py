from flask import Flask
import os

from flask_smorest import Api
from db import db
from flask_jwt_extended import JWTManager

from resources.pet import blp as PetBlueprint  
from resources.owner import blp as OwnerBlueprint  
from resources.user import blp as UserBlueprint 
from flask import jsonify 
from blocklist import BLOCKLIST
from flask_migrate import Migrate


def create_app(db_url=None):
    app=Flask(__name__)

    app.config["PROPAGATE_EXCEPTION"]=True
    app.config["API_TITLE"]="Stores REST API"
    app.config["API_VERSION"]="v1"
    app.config["OPENAPI_VERSION"]="3.0.3"
    app.config["OPENAPI_URL_PREFIX"]="/"
    app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"]="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"]= db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
    
    db.init_app(app)

    migrate = Migrate(app, db)

    api=Api(app)

    app.config["JWT_SECRET_KEY"] = "68050107548169146128503416861773923812"
    jwt= JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"description":"The token has been revoked.", "error":"token_revoked"}
            ), 401
        )  


    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"description":"The token is not fresh.", "error":"refresh_tokn_required"}
            ), 401
        )

          

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({"message": "The token has expired", "error": "token_expired"}), 401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(
            jsonify({"message": "Signature Verification Failed", "error": "invalid_token"}), 401,
        )   

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify({"description": "Request does not contain an access token", "error": "authorization_required"}), 401,
        )     

    @app.before_first_request
    def create_tables():
        db.create_all()



    api.register_blueprint(OwnerBlueprint)
    api.register_blueprint(PetBlueprint)
    api.register_blueprint(UserBlueprint)

    return app