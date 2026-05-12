from datetime import datetime
from marshmallow  import Schema, fields
from db import db

from models.ligne_vente import LigneVenteSchema;


class VenteModel(db.Model):
    __tablename__ = "tbl_vente"

    vente_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    entreprise_id = db.Column(
        db.Integer,
        db.ForeignKey("tbl_entreprise.entreprise_id"),
        nullable=False
    )

    distribution_id = db.Column(
        db.Integer,
        db.ForeignKey("tbl_distribution.distribution_id"),
        nullable=False
    )

    cree_par = db.Column(
        db.Integer,
        nullable=True
    )

    cree_le = db.Column(
        db.DateTime,
        nullable=True
    )

    lignes = db.relationship(
        "LigneVenteModel",
        backref="vente",
        lazy=True,
        cascade="all, delete-orphan"
    )




class VenteSchema(Schema):

    vente_id = fields.Int(
        dump_only=True
    )

    entreprise_id = fields.Int(
        required=True
    )

    distribution_id = fields.Int(
        required=True
    )

    cree_par = fields.Int(
        allow_none=True
    )

    cree_le = fields.DateTime(
        dump_only=True
    )

    # 🔥 THIS IS REQUIRED
    lignes = fields.Nested(LigneVenteSchema,many=True)


