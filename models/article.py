from datetime import datetime
from marshmallow  import Schema, fields
from db import db

class ArticleModel(db.Model):
    __tablename__ = "tbl_article"

    article_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    article_code = db.Column(db.String(45), unique=True, nullable=False)
    article_desc = db.Column(db.String(60), unique=True, nullable=False)

    categorie_id = db.Column(
        db.Integer,
        db.ForeignKey("tbl_categorie.categorie_id"),
        nullable=False
    )

    cree_par = db.Column(db.Integer, nullable=True)
    cree_le = db.Column(db.DateTime, nullable=True)

    modifie_par = db.Column(db.Integer, nullable=True)
    modifie_le = db.Column(db.DateTime, nullable=True)



class ArticleSchema(Schema):
    article_id = fields.Int(dump_only=True)

    article_code = fields.Str(required=True)
    article_desc = fields.Str(required=True)

    categorie_id = fields.Int(required=True)

    cree_par = fields.Int(allow_none=True)
    cree_le = fields.DateTime(allow_none=True)

    modifie_par = fields.Int(allow_none=True)
    modifie_le = fields.DateTime(allow_none=True)