from datetime import datetime
from marshmallow  import Schema, fields
from db import db



class AchatModel(db.Model):
    __tablename__ = "tbl_achat"

    achat_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    entreprise_id = db.Column(
        db.Integer,
        db.ForeignKey("tbl_entreprise.entreprise_id"),
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

    quantite = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    prix_unitaire = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    transport_sur_achat = db.Column(
        db.Numeric(10, 2),
        nullable=True,
        default=0.00
    )

    rendu_rabais_sur_achat = db.Column(
        db.Numeric(10, 2),
        nullable=True,
        default=0.00
    )

    cout_total = db.Column(
        db.Numeric(10, 2),
        nullable=True,
        default=0.00
    )

    cree_par = db.Column(
        db.Integer,
        nullable=True
    )

    cree_le = db.Column(
        db.DateTime,
        nullable=True
    )

    modifie_par = db.Column(
        db.Integer,
        nullable=True
    )

    modifie_le = db.Column(
        db.DateTime,
        nullable=True
    )

    def __repr__(self):
        return f"<Achat {self.achat_id}>"

    def to_dict(self):
        return {
            "achat_id": self.achat_id,
            "entreprise_id": self.entreprise_id,
            "categorie_id": self.categorie_id,
            "article_id": self.article_id,
            "quantite": str(self.quantite),
            "prix_unitaire": str(self.prix_unitaire),
            "transport_sur_achat": str(self.transport_sur_achat),
            "rendu_rabais_sur_achat": str(self.rendu_rabais_sur_achat),
            "cout_total": str(self.cout_total),
            "cree_par": self.cree_par
        }



from marshmallow import Schema, fields


class AchatSchema(Schema):

    achat_id = fields.Int(dump_only=True)

    entreprise_id = fields.Int(required=True)

    categorie_id = fields.Int(required=True)

    article_id = fields.Int(required=True)

    quantite = fields.Decimal(
        required=True,
        as_string=True
    )

    prix_unitaire = fields.Decimal(
        required=True,
        as_string=True
    )

    transport_sur_achat = fields.Decimal(
        as_string=True,
        allow_none=True
    )

    rendu_rabais_sur_achat = fields.Decimal(
        as_string=True,
        allow_none=True
    )

    cout_total = fields.Decimal(
        dump_only=True,
        as_string=True
    )

    cree_par = fields.Int(
        allow_none=True
    )

    cree_le = fields.DateTime(
        allow_none=True
    )

    modifie_par = fields.Int(
        allow_none=True
    )

    modifie_le = fields.DateTime(
        allow_none=True
    )