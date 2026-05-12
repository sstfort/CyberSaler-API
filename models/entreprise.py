from datetime import datetime
from marshmallow  import Schema, fields
from db import db

class EntrepriseModel(db.Model):
    __tablename__ = "tbl_entreprise"

    entreprise_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    nom_commercial = db.Column(db.String(45), unique=True, nullable=False)
    contact = db.Column(db.String(120), nullable=False)
    adresse = db.Column(db.String(125), nullable=False)

    tel1 = db.Column(db.String(12), nullable=False)
    tel2 = db.Column(db.String(12), nullable=True)

    email = db.Column(db.String(125), nullable=True)
    site = db.Column(db.String(45), nullable=True)

    cree_par = db.Column(db.Integer, nullable=True)
    cree_le = db.Column(db.DateTime, nullable=True)

    modifie_par = db.Column(db.Integer, nullable=True)
    modifie_le = db.Column(db.DateTime, nullable=True)

    def __init__(self, nom_commercial, contact, adresse, tel1,
                 tel2=None, email=None, site=None,
                 cree_par=None, modifie_par=None):
        self.nom_commercial = nom_commercial
        self.contact = contact
        self.adresse = adresse
        self.tel1 = tel1
        self.tel2 = tel2
        self.email = email
        self.site = site
        self.cree_par = cree_par
        self.modifie_par = modifie_par

    def __repr__(self):
        return f"<Entreprise {self.nom_commercial}>"



class EntrepriseSchema(Schema):
    entreprise_id = fields.Int(dump_only=True)

    nom_commercial = fields.Str(required=True)
    contact = fields.Str(required=True)
    adresse = fields.Str(required=True)

    tel1 = fields.Str(required=True)
    tel2 = fields.Str(allow_none=True)

    email = fields.Email(allow_none=True)
    site = fields.Str(allow_none=True)

    cree_par = fields.Int(allow_none=True)
    cree_le = fields.DateTime(dump_only=True)

    modifie_par = fields.Int(allow_none=True)
    modifie_le = fields.DateTime(dump_only=True)