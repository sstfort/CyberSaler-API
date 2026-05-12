from datetime import datetime
from marshmallow  import Schema, fields
from db import db



class LevelModel(db.Model):
    __tablename__ = "tbl_level"

    level_id = db.Column(
        db.Integer,
        primary_key=True
    )

    level_name = db.Column(
        db.String(45),
        nullable=False
    )

    def __repr__(self):
        return f"<Level {self.level_name}>"

    def to_dict(self):
        return {
            "level_id": self.level_id,
            "level_name": self.level_name
        }




class LevelSchema(Schema):

    level_id = fields.Int(required=True)

    level_name = fields.Str(required=True)