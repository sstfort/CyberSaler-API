from datetime import datetime
from marshmallow  import Schema, fields
from db import db


class PrixVenteModel(db.Model):
    __tablename__ = "tbl_prix_vente"

    prix_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

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

    categorie_id = db.Column(
        db.Integer,
        db.ForeignKey("tbl_categorie.categorie_id"),
        nullable=False
    )

    article_id = db.Column(
        db.Integer,
        db.ForeignKey("tbl_article.article_id"),
        nullable=False
    )

    prix_vente = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    cree_par = db.Column(db.Integer, nullable=True)
    cree_le = db.Column(db.DateTime, nullable=True)

    modifie_par = db.Column(db.Integer, nullable=True)
    modifie_le = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.UniqueConstraint(
            "entreprise_id",
            "distribution_id",
            "categorie_id",
            "article_id",
            name="prix_unique"
        ),
    )




class PrixVenteSchema(Schema):
    prix_id = fields.Int(dump_only=True)

    entreprise_id = fields.Int(required=True)
    distribution_id = fields.Int(required=True)
    categorie_id = fields.Int(required=True)
    article_id = fields.Int(required=True)

    prix_vente = fields.Decimal(
        required=True,
        as_string=True
    )

    cree_par = fields.Int(allow_none=True)
    cree_le = fields.DateTime(allow_none=True)

    modifie_par = fields.Int(allow_none=True)
    modifie_le = fields.DateTime(allow_none=True)