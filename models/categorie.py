from datetime import datetime
from marshmallow  import Schema, fields
from db import db

class CategorieModel(db.Model):
    __tablename__ = "tbl_categorie"

    categorie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    categorie_code = db.Column(db.String(45), unique=True, nullable=False)
    categorie_desc = db.Column(db.String(60), unique=True, nullable=False)

    val_unit_cigle = db.Column(db.String(2), nullable=False)
    val_unit_nom = db.Column(db.String(20), nullable=False)

    cree_par = db.Column(db.Integer, nullable=True)
    cree_le = db.Column(db.DateTime, nullable=True)

    modifie_par = db.Column(db.Integer, nullable=True)
    modifie_le = db.Column(db.DateTime, nullable=True)



class CategorieSchema(Schema):
    categorie_id = fields.Int(dump_only=True)

    categorie_code = fields.Str(required=True)
    categorie_desc = fields.Str(required=True)

    val_unit_cigle = fields.Str(required=True)
    val_unit_nom = fields.Str(required=True)

    cree_par = fields.Int(allow_none=True)
    cree_le = fields.DateTime(allow_none=True)

    modifie_par = fields.Int(allow_none=True)
    modifie_le = fields.DateTime(allow_none=True)