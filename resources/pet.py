from flask_jwt_extended import jwt_required
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import PetModel
from db import db
from sqlalchemy.exc import SQLAlchemyError

from schemas import PetSchema, PetUpdateSchema


blp=Blueprint("Pets", __name__, description="Operations on pets")

@blp.route("/pet/<int:pet_id>")
class Pet(MethodView):
    @jwt_required()
    @blp.response(200, PetSchema)
    def get(self, pet_id):
        pet = PetModel.query.get_or_404(pet_id) 
        return pet

    @jwt_required()
    def delete(self,pet_id):
        pet = PetModel.query.get_or_404(pet_id) 
        db.session.delete(pet)
        db.session.commit()
        return{"message":"Pet Deleted"}

    @jwt_required()
    @blp.arguments(PetUpdateSchema)
    @blp.response(200,PetSchema)
    def put(self,pet_data, pet_id):
        pet = PetModel.query.get_or_404(pet_id) 
        if pet:
            pet.name = pet_data["name"]
            pet.breed = pet_data["breed"]  
        else:
            pet = PetModel(id=pet_id,**pet_data)

        db.session.add(pet)
        db.session.commit()

        return pet              

@blp.route("/pet")
class PetList(MethodView):
    @jwt_required()
    @blp.response(200, PetSchema(many=True))
    def get(self):
        return PetModel.query.all()

    
    @jwt_required()
    @blp.arguments(PetSchema)
    @blp.response(201, PetSchema)
    def post(self, pet_data):
        pet = PetModel(**pet_data)
        try:
            db.session.add(pet)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occured while inserting the pet")
        return pet, 201        
    