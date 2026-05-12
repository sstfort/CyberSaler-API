from datetime import datetime
from marshmallow  import Schema, fields
from db import db
from models.ligne_vente import LigneVenteSchema


class VenteCompleteSchema(Schema):

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

    cree_le = fields.Int(
        dump_only=True
    )

    lignes = fields.List(
        fields.Nested(LigneVenteSchema),
        required=True
    )