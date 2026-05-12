from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flask_jwt_extended import jwt_required

from db import db

from models.vente import VenteModel, VenteSchema
from models.ligne_vente import LigneVenteModel

from models.entreprise import EntrepriseModel
from models.distribution import DistributionModel
from models.categorie import CategorieModel
from models.article import ArticleModel

from models.vente_complet import VenteCompleteSchema


blp = Blueprint(
    "vente_complete",
    __name__,
    description="Operations on vente with lignes"
)



@blp.route("/vente-complete")
class VenteCompleteResource(MethodView):

    @jwt_required()
    @blp.arguments(VenteSchema)
    @blp.response(201, VenteSchema)
    def post(self, data):

        vente = VenteModel(
            entreprise_id=data["entreprise_id"],
            distribution_id=data["distribution_id"],
            cree_par=data["cree_par"]
        )

        db.session.add(vente)
        db.session.flush()  # generate vente_id

        lignes_response = []

        for item in data["lignes"]:

            ligne = LigneVenteModel(
                vente_id=vente.vente_id,
                entreprise_id=data["entreprise_id"],
                distribution_id=data["distribution_id"],
                categorie_id=item["categorie_id"],
                article_id=item["article_id"],
                quantite=item["quantite"]
            )

            db.session.add(ligne)
            lignes_response.append(ligne)

        db.session.commit()

        vente = db.session.query(VenteModel)\
            .options(db.joinedload(VenteModel.lignes))\
            .get(vente.vente_id)

        return vente