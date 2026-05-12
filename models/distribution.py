from datetime import datetime
from marshmallow  import Schema, fields
from db import db

class DistributionModel(db.Model):
    __tablename__ = "tbl_distribution"

    distribution_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    entreprise_id = db.Column(db.Integer, db.ForeignKey("tbl_entreprise.entreprise_id"), nullable=False)
    entreprise = db.relationship("EntrepriseModel", backref="distributions")

    adresse = db.Column(db.String(120), nullable=True)

    tel1 = db.Column(db.String(11), nullable=True)
    tel2 = db.Column(db.String(11), nullable=True)

    cree_par = db.Column(db.Integer, nullable=True)
    cree_le = db.Column(db.DateTime, nullable=True)

    modifie_par = db.Column(db.Integer, nullable=True)
    modifie_le = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Distribution {self.distribution_id} - Entreprise {self.entreprise_id}>"

    def to_dict(self):
        return {
            "distribution_id": self.distribution_id,
            "entreprise_id": self.entreprise_id,
            "adresse": self.adresse,
            "tel1": self.tel1,
            "tel2": self.tel2,
            "cree_par": self.cree_par,
            "cree_le": self.cree_le.isoformat() if self.cree_le else None,
            "modifie_par": self.modifie_par,
            "modifie_le": self.modifie_le.isoformat() if self.modifie_le else None,
        }



class DistributionSchema(Schema):
    distribution_id = fields.Int(dump_only=True)

    entreprise_id = fields.Int(required=True)

    adresse = fields.Str(allow_none=True)

    tel1 = fields.Str(allow_none=True)
    tel2 = fields.Str(allow_none=True)

    cree_par = fields.Int(allow_none=True)
    cree_le = fields.DateTime(allow_none=True)

    modifie_par = fields.Int(allow_none=True)
    modifie_le = fields.DateTime(allow_none=True)