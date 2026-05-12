from decimal import Decimal

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy import text

from db import db

from models.achat import AchatModel
from models.article import ArticleModel
from models.categorie import CategorieModel
from models.entreprise import EntrepriseModel

from models.achat import AchatSchema

blp = Blueprint(
    "achats",
    __name__,
    description="Operations on achats"
)


@blp.route("/achat")
class AchatListResource(MethodView):

    @jwt_required()
    @blp.response(200, AchatSchema(many=True))
    def get(self):
        return AchatModel.query.all()

    @jwt_required()
    @blp.arguments(AchatSchema)
    @blp.response(201, AchatSchema)
    def post(self, data):
            
        # ✅ FK validations
        if not EntrepriseModel.query.get(data["entreprise_id"]):
            abort(400, message="Invalid entreprise_id")

        if not CategorieModel.query.get(data["categorie_id"]):
            abort(400, message="Invalid categorie_id")

        if not ArticleModel.query.get(data["article_id"]):
            abort(400, message="Invalid article_id")

        # ✅ calculate total cost
        quantite = Decimal(data["quantite"])
        prix_unitaire = Decimal(data["prix_unitaire"])

        transport = Decimal(
            data.get("transport_sur_achat") or 0
        )

        rabais = Decimal(
            data.get("rendu_rabais_sur_achat") or 0
        )

        data["cout_total"] = (
            (quantite * prix_unitaire)
            + transport
            - rabais
        )

        achat = AchatModel(**data)
        
        result = db.session.execute(text("SELECT DATABASE()"))

        print(result.fetchone())

        try:
            db.session.add(achat)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return achat


@blp.route("/achat/<int:achat_id>")
class AchatResource(MethodView):

    @jwt_required()
    @blp.response(200, AchatSchema)
    def get(self, achat_id):
        return AchatModel.query.get_or_404(achat_id)

    @jwt_required()
    def delete(self, achat_id):

        achat = AchatModel.query.get_or_404(achat_id)

        db.session.delete(achat)
        db.session.commit()

        return {"message": "Achat deleted"}, 200

    @jwt_required()
    @blp.arguments(AchatSchema)
    @blp.response(200, AchatSchema)
    def put(self, data, achat_id):

        achat = AchatModel.query.get(achat_id)

        # ✅ FK validations
        if not EntrepriseModel.query.get(data["entreprise_id"]):
            abort(400, message="Invalid entreprise_id")

        if not CategorieModel.query.get(data["categorie_id"]):
            abort(400, message="Invalid categorie_id")

        if not ArticleModel.query.get(data["article_id"]):
            abort(400, message="Invalid article_id")

        # ✅ recalculate total
        quantite = Decimal(data["quantite"])
        prix_unitaire = Decimal(data["prix_unitaire"])

        transport = Decimal(
            data.get("transport_sur_achat") or 0
        )

        rabais = Decimal(
            data.get("rendu_rabais_sur_achat") or 0
        )

        data["cout_total"] = (
            (quantite * prix_unitaire)
            + transport
            - rabais
        )

        if achat:
            for key, value in data.items():
                setattr(achat, key, value)
        else:
            achat = AchatModel(**data)

        try:
            db.session.add(achat)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return achat