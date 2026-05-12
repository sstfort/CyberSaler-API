from datetime import datetime
from marshmallow  import Schema, fields
from db import db


class LigneVenteModel(db.Model):
    __tablename__ = "tbl_ligne_vente"

    ligne_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    vente_id = db.Column(
        db.Integer,
        db.ForeignKey("tbl_vente.vente_id"),
        nullable=False
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

    prix_vente_id = db.Column(
        db.Integer,
        db.ForeignKey("tbl_prix_vente.prix_id"),
        nullable=True
    )

    prix_vente = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )

    quantite = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )

    unite = db.Column(
        db.String(2),
        nullable=True
    )

    cout_vente_total = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )

    cree_par = db.Column(
        db.Integer,
        nullable=True
    )

    cree_le = db.Column(
        db.DateTime,
        nullable=True
    )

    def __repr__(self):
        return f"<LigneVente {self.ligne_id}>"

    def to_dict(self):
        return {
            "ligne_id": self.ligne_id,
            "entreprise_id": self.entreprise_id,
            "distribution_id": self.distribution_id,
            "categorie_id": self.categorie_id,
            "article_id": self.article_id,
            "prix_vente_id": self.prix_vente_id,
            "prix_vente": str(self.prix_vente) if self.prix_vente else None,
            "quantite": str(self.quantite) if self.quantite else None,
            "unite": self.unite,
            "cout_vente_total": str(self.cout_vente_total) if self.cout_vente_total else None,
            "cree_par": self.cree_par
        }



class LigneVenteSchema(Schema):
    ligne_id = fields.Int(dump_only=True)
    categorie_id = fields.Int()
    article_id = fields.Int()
    quantite = fields.Decimal(as_string=True)
    unite = fields.Str(dump_only=True)
    prix_vente = fields.Decimal(dump_only=True)
    cout_vente_total = fields.Decimal(dump_only=True)