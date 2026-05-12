from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flask_jwt_extended import jwt_required

from db import db

from models.ligne_vente import LigneVenteModel
from models.entreprise import EntrepriseModel
from models.distribution import DistributionModel
from models.categorie import CategorieModel
from models.article import ArticleModel

from models.ligne_vente import LigneVenteSchema


blp = Blueprint(
    "ligne_ventes",
    __name__,
    description="Operations on ligne ventes"
)


@blp.route("/ligne-vente")
class LigneVenteListResource(MethodView):

    @jwt_required()
    @blp.response(200, LigneVenteSchema(many=True))
    def get(self):

        return LigneVenteModel.query.all()

    @jwt_required()
    @blp.arguments(LigneVenteSchema)
    @blp.response(201, LigneVenteSchema)
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

        if not CategorieModel.query.get(
            data["categorie_id"]
        ):
            abort(
                400,
                message="Invalid categorie_id"
            )

        if not ArticleModel.query.get(
            data["article_id"]
        ):
            abort(
                400,
                message="Invalid article_id"
            )

        ligne = LigneVenteModel(
            entreprise_id=data["entreprise_id"],
            distribution_id=data["distribution_id"],
            categorie_id=data["categorie_id"],
            article_id=data["article_id"],
            quantite=data["quantite"],
            unite=data["unite"],
            cree_par=data.get("cree_par")
        )

        try:

            db.session.add(ligne)
            db.session.commit()

        except Exception as e:

            db.session.rollback()

            abort(
                500,
                message=str(e)
            )

        return ligne


@blp.route("/ligne-vente/<int:ligne_id>")
class LigneVenteResource(MethodView):

    @jwt_required()
    @blp.response(200, LigneVenteSchema)
    def get(self, ligne_id):

        return LigneVenteModel.query.get_or_404(
            ligne_id
        )

    @jwt_required()
    def delete(self, ligne_id):

        ligne = LigneVenteModel.query.get_or_404(
            ligne_id
        )

        db.session.delete(ligne)

        db.session.commit()

        return {
            "message": "Ligne vente deleted"
        }, 200

    @jwt_required()
    @blp.arguments(LigneVenteSchema)
    @blp.response(200, LigneVenteSchema)
    def put(self, data, ligne_id):

        ligne = LigneVenteModel.query.get_or_404(
            ligne_id
        )

        ligne.entreprise_id = data[
            "entreprise_id"
        ]

        ligne.distribution_id = data[
            "distribution_id"
        ]

        ligne.categorie_id = data[
            "categorie_id"
        ]

        ligne.article_id = data[
            "article_id"
        ]

        ligne.quantite = data[
            "quantite"
        ]

        ligne.unite = data[
            "unite"
        ]

        ligne.cree_par = data.get(
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

        return ligne