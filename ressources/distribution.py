from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from db import db
from models.distribution import DistributionModel, DistributionSchema
from models.entreprise import EntrepriseModel

blp = Blueprint(
    "distributions",
    __name__,
    description="Operations on distributions"
)

distribution_schema = DistributionSchema()
distributions_schema = DistributionSchema(many=True)


@blp.route("/distribution")
class DistributionListResource(MethodView):

    @jwt_required()
    @blp.response(200, DistributionSchema(many=True))
    def get(self):
        return DistributionModel.query.all()

    @jwt_required()
    @blp.arguments(DistributionSchema)
    @blp.response(201, DistributionSchema)
    def post(self, data):

        if not EntrepriseModel.query.get(data["entreprise_id"]):
            abort(400, message="Invalid entreprise_id")

        distribution = DistributionModel(**data)

        try:
            db.session.add(distribution)
            db.session.commit()
        except Exception as e:
            abort(500, message=str(e))

        return distribution


@blp.route("/distribution/<int:distribution_id>")
class DistributionResource(MethodView):

    @jwt_required()
    @blp.response(200, DistributionSchema)
    def get(self, distribution_id):
        distribution = DistributionModel.query.get_or_404(distribution_id)
        return distribution

    @jwt_required()
    def delete(self, distribution_id):
        distribution = DistributionModel.query.get_or_404(distribution_id)

        db.session.delete(distribution)
        db.session.commit()

        return {"message": "Distribution deleted"}, 200

    @jwt_required()
    @blp.arguments(DistributionSchema)
    @blp.response(200, DistributionSchema)
    def put(self, data, distribution_id):
        distribution = DistributionModel.query.get(distribution_id)

        if distribution:
            for key, value in data.items():
                setattr(distribution, key, value)
        else:
            distribution = DistributionModel(**data)

        try:
            db.session.add(distribution)
            db.session.commit()
        except Exception as e:
            abort(500, message=str(e))

        return distribution