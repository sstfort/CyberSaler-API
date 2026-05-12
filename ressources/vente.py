from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flask_jwt_extended import jwt_required

from db import db

from models.vente import VenteModel
from models.entreprise import EntrepriseModel
from models.distribution import DistributionModel

from models.vente import VenteSchema


blp = Blueprint(
    "ventes",
    __name__,
    description="Operations on ventes"
)


@blp.route("/vente")
class VenteListResource(MethodView):

    @jwt_required()
    @blp.response(200, VenteSchema(many=True))
    def get(self):

        return VenteModel.query.all()

    @jwt_required()
    @blp.arguments(VenteSchema)
    @blp.response(201, VenteSchema)
    def post(self, data):

        if not EntrepriseModel.query.get(
            data["entreprise_id"]
        ):
            abort(
                400,
                message="Invalid entreprise_id"
            )

        if not DistributionModel.query.get(
            data["distribution_id"]
        ):
            abort(
                400,
                message="Invalid distribution_id"
            )

        vente = VenteModel(
            entreprise_id=data["entreprise_id"],
            distribution_id=data["distribution_id"],
            cree_par=data.get("cree_par")
        )

        try:

            db.session.add(vente)
            db.session.commit()

        except Exception as e:

            db.session.rollback()

            abort(
                500,
                message=str(e)
            )

        return vente


@blp.route("/vente/<int:vente_id>")
class VenteResource(MethodView):

    @jwt_required()
    @blp.response(200, VenteSchema)
    def get(self, vente_id):

        return VenteModel.query.get_or_404(
            vente_id
        )

    @jwt_required()
    def delete(self, vente_id):

        vente = VenteModel.query.get_or_404(
            vente_id
        )

        db.session.delete(vente)

        db.session.commit()

        return {
            "message": "Vente deleted"
        }, 200

    @jwt_required()
    @blp.arguments(VenteSchema)
    @blp.response(200, VenteSchema)
    def put(self, data, vente_id):

        vente = VenteModel.query.get_or_404(
            vente_id
        )

        vente.entreprise_id = data[
            "entreprise_id"
        ]

        vente.distribution_id = data[
            "distribution_id"
        ]

        vente.cree_par = data.get(
            "cree_par"
        )

        try:

            db.session.commit()

        except Exception as e:

            db.session.rollback()

            abort(
                500,
                message=str(e)
            )

        return vente