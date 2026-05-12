from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from db import db

from models.prix_vente import PrixVenteModel
from models.entreprise import EntrepriseModel
from models.distribution import DistributionModel
from models.categorie import CategorieModel
from models.article import ArticleModel

from models.prix_vente import PrixVenteSchema

blp = Blueprint(
    "prix_vente",
    __name__,
    description="Operations on prix vente"
)


@blp.route("/prix-vente")
class PrixVenteListResource(MethodView):

    @jwt_required()
    @blp.response(200, PrixVenteSchema(many=True))
    def get(self):
        return PrixVenteModel.query.all()

    @jwt_required()
    @blp.arguments(PrixVenteSchema)
    @blp.response(201, PrixVenteSchema)
    def post(self, data):

        # ✅ FK validations
        if not EntrepriseModel.query.get(data["entreprise_id"]):
            abort(400, message="Invalid entreprise_id")

        if not DistributionModel.query.get(data["distribution_id"]):
            abort(400, message="Invalid distribution_id")

        if not CategorieModel.query.get(data["categorie_id"]):
            abort(400, message="Invalid categorie_id")

        if not ArticleModel.query.get(data["article_id"]):
            abort(400, message="Invalid article_id")

        # ✅ unique validation
        exists = PrixVenteModel.query.filter_by(
            entreprise_id=data["entreprise_id"],
            distribution_id=data["distribution_id"],
            categorie_id=data["categorie_id"],
            article_id=data["article_id"]
        ).first()

        if exists:
            abort(
                400,
                message="Prix vente already exists for this combination"
            )

        prix_vente = PrixVenteModel(**data)

        try:
            db.session.add(prix_vente)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return prix_vente
    


@blp.route("/prix-vente/<int:prix_id>")
class PrixVenteResource(MethodView):

    @jwt_required()
    @blp.response(200, PrixVenteSchema)
    def get(self, prix_id):
        return PrixVenteModel.query.get_or_404(prix_id)

    @jwt_required()
    def delete(self, prix_id):

        prix_vente = PrixVenteModel.query.get_or_404(prix_id)

        db.session.delete(prix_vente)
        db.session.commit()

        return {"message": "Prix vente deleted"}, 200

    @jwt_required()
    @blp.arguments(PrixVenteSchema)
    @blp.response(200, PrixVenteSchema)
    def put(self, data, prix_id):

        prix_vente = PrixVenteModel.query.get(prix_id)

        # ✅ FK validations
        if not EntrepriseModel.query.get(data["entreprise_id"]):
            abort(400, message="Invalid entreprise_id")

        if not DistributionModel.query.get(data["distribution_id"]):
            abort(400, message="Invalid distribution_id")

        if not CategorieModel.query.get(data["categorie_id"]):
            abort(400, message="Invalid categorie_id")

        if not ArticleModel.query.get(data["article_id"]):
            abort(400, message="Invalid article_id")

        # ✅ unique validation
        exists = PrixVenteModel.query.filter(
            PrixVenteModel.entreprise_id == data["entreprise_id"],
            PrixVenteModel.distribution_id == data["distribution_id"],
            PrixVenteModel.categorie_id == data["categorie_id"],
            PrixVenteModel.article_id == data["article_id"],
            PrixVenteModel.prix_id != prix_id
        ).first()

        if exists:
            abort(
                400,
                message="Prix vente already exists for this combination"
            )

        if prix_vente:
            for key, value in data.items():
                setattr(prix_vente, key, value)
        else:
            prix_vente = PrixVenteModel(**data)

        try:
            db.session.add(prix_vente)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return prix_vente