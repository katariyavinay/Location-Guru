from pydoc import describe
from db import db

class PetModel(db.Model):
    __tablename__="pets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String)
    breed = db.Column(db.String(80), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.id"), unique=False, nullable=False)
    owner = db.relationship("OwnerModel", back_populates="pets")