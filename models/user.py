from datetime import datetime
from marshmallow  import Schema, fields
from db import db


class UserModel(db.Model):
    __tablename__ = "tbl_users"

    user_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    nom_prenom = db.Column(
        db.String(120),
        nullable=True
    )

    username = db.Column(
        db.String(45),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    entreprise_id = db.Column(
        db.Integer,
        db.ForeignKey("tbl_entreprise.entreprise_id"),
        nullable=True
    )

    distribution_id = db.Column(
        db.Integer,
        db.ForeignKey("tbl_distribution.distribution_id"),
        nullable=True
    )

    level_id = db.Column(
        db.Integer,
        db.ForeignKey("tbl_level.level_id"),
        nullable=False
    )

    statut_user = db.Column(
        db.Boolean,
        nullable=True,
        default=False
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
        "modifie_Le",
        db.DateTime,
        nullable=True
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "nom_prenom": self.nom_prenom,
            "username": self.username,
            "entreprise_id": self.entreprise_id,
            "distribution_id": self.distribution_id,
            "level_id": self.level_id,
            "statut_user": self.statut_user
        }



class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)

    nom_prenom = fields.Str(allow_none=True)

    username = fields.Str(required=True)

    password = fields.Str(
        required=True,
        load_only=True
    )

    entreprise_id = fields.Int(allow_none=True)

    distribution_id = fields.Int(allow_none=True)

    level_id = fields.Int(required=True)

    statut_user = fields.Bool(allow_none=True)

    cree_par = fields.Int(allow_none=True)
    cree_le = fields.DateTime(allow_none=True)

    modifie_par = fields.Int(allow_none=True)
    modifie_le = fields.DateTime(allow_none=True)




class UserLoginSchema(Schema):

    username = fields.Str(required=True)

    password = fields.Str(
        required=True,
        load_only=True
    )


from marshmallow import Schema, fields


class UserChangePwdSchema(Schema):

    username = fields.Str(
        required=True
    )

    old_password = fields.Str(
        required=True
    )

    new_password = fields.Str(
        required=True
    )