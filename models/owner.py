from db import db

class OwnerModel(db.Model):
    __tablename__="owners"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    pets = db.relationship("PetModel", back_populates="owner", lazy="dynamic")
    # user = db.relationship("UserModel", back_populates="owners")
  