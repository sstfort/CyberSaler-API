from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from db import db
from models.entreprise import EntrepriseModel, EntrepriseSchema

blp = Blueprint("entreprises", __name__, description="Operations on entreprises")

entreprise_schema = EntrepriseSchema()
entreprises_schema = EntrepriseSchema(many=True)


@blp.route("/entreprise/<int:entreprise_id>")
class EntrepriseResource(MethodView):

    @jwt_required()
    @blp.response(200, EntrepriseSchema)
    def get(self, entreprise_id):
        entreprise = EntrepriseModel.query.get_or_404(entreprise_id)
        return entreprise

    @jwt_required()
    def delete(self, entreprise_id):
        entreprise = EntrepriseModel.query.get_or_404(entreprise_id)
        db.session.delete(entreprise)
        db.session.commit()
        return {"message": "Entreprise deleted"}, 200

    @jwt_required()
    @blp.arguments(EntrepriseSchema)
    @blp.response(200, EntrepriseSchema)
    def put(self, data, entreprise_id):
        entreprise = EntrepriseModel.query.get(entreprise_id)

        if entreprise:
            # update
            for key, value in data.items():
                setattr(entreprise, key, value)
        else:
            # create
            entreprise = EntrepriseModel(**data)

        try:
            db.session.add(entreprise)
            db.session.commit()
        except Exception as e:
            abort(500, message=str(e))

        return entreprise


@blp.route("/entreprise")
class EntrepriseListResource(MethodView):

    @jwt_required()
    @blp.response(200, EntrepriseSchema(many=True))
    def get(self):
        return EntrepriseModel.query.all()

    @jwt_required()
    @blp.arguments(EntrepriseSchema)
    @blp.response(201, EntrepriseSchema)
    def post(self, data):
        # 🔒 check unique nom_commercial
        if EntrepriseModel.query.filter_by(nom_commercial=data["nom_commercial"]).first():
            abort(400, message="nom_commercial already exists")

        entreprise = EntrepriseModel(**data)

        try:
            db.session.add(entreprise)
            db.session.commit()
        except Exception as e:
            abort(500, message=str(e))

        return entreprise