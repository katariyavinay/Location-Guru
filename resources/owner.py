from sqlite3 import IntegrityError
from flask_jwt_extended import jwt_required
from db import db 
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import OwnerModel
from schemas import OwnerSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError



blp=Blueprint("owners", __name__, description="Operations on owners")

@blp.route("/owner/<int:owner_id>")
class Owner(MethodView):
    @jwt_required()
    @blp.response(201, OwnerSchema)
    def get(self, owner_id):
        owner = OwnerModel.query.get_or_404(owner_id)
        return owner

    @jwt_required()
    def delete(self,  owner_id):
        owner = OwnerModel.query.get_or_404(owner_id)
        db.session.delete(owner)
        db.session.commit()

        return{"message":"Owner Deleted"}

@blp.route("/owner")
class OwnerList(MethodView):
    @jwt_required()
    @blp.response(200, OwnerSchema(many=True))
    def get(self):
        return OwnerModel.query.all()

    @jwt_required()
    @blp.arguments(OwnerSchema)
    @blp.response(200, OwnerSchema)
    def post(self, owner_data):       
        owner = OwnerModel(**owner_data)
        try:
            db.session.add(owner)
            db.session.commit()
        except IntegrityError:
            abort(400,
            message="A owner with that name already exists.",)
        except SQLAlchemyError:
            abort(500,
            message="An error occured creating the owner.",)                
        return owner, 201                