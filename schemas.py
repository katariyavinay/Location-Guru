from dbm import dumb
from importlib.metadata import requires
from operator import truediv
from marshmallow import Schema, fields

class PlainPetSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required=True)
    breed = fields.Str(required = True)
    
class PlainOwnerSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required=True)

class PetUpdateSchema(Schema):
    name = fields.Str()
    breed = fields.Str()
    pet_id = fields.Int()
    
class PetSchema(PlainPetSchema):
    owner_id = fields.Int(required=True, load_only=True)
    owner = fields.Nested(PlainOwnerSchema(), dump_only = True)

class OwnerSchema(PlainOwnerSchema):
    pets= fields.List(fields.Nested(PlainPetSchema()), dumb_only=True)



class UserSchema(Schema):
    id = fields.Int(dump_only = True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)