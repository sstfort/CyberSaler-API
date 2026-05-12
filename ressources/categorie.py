from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from db import db
from models.categorie import CategorieModel
from models.categorie import CategorieSchema

blp = Blueprint(
    "categories",
    __name__,
    description="Operations on categories"
)

categorie_schema = CategorieSchema()
categories_schema = CategorieSchema(many=True)

@blp.route("/categorie")
class CategorieListResource(MethodView):

    @jwt_required()
    @blp.response(200, CategorieSchema(many=True))
    def get(self):
        return CategorieModel.query.all()

    @jwt_required()
    @blp.arguments(CategorieSchema)
    @blp.response(201, CategorieSchema)
    def post(self, data):

        # ✅ unique checks
        if CategorieModel.query.filter_by(categorie_code=data["categorie_code"]).first():
            abort(400, message="categorie_code already exists")

        if CategorieModel.query.filter_by(categorie_desc=data["categorie_desc"]).first():
            abort(400, message="categorie_desc already exists")

        categorie = CategorieModel(**data)

        try:
            db.session.add(categorie)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return categorie


@blp.route("/categorie/<int:categorie_id>")
class CategorieResource(MethodView):

    @jwt_required()
    @blp.response(200, CategorieSchema)
    def get(self, categorie_id):
        return CategorieModel.query.get_or_404(categorie_id)

    @jwt_required()
    def delete(self, categorie_id):
        categorie = CategorieModel.query.get_or_404(categorie_id)

        db.session.delete(categorie)
        db.session.commit()

        return {"message": "Categorie deleted"}, 200

    @jwt_required()
    @blp.arguments(CategorieSchema)
    @blp.response(200, CategorieSchema)
    def put(self, data, categorie_id):

        categorie = CategorieModel.query.get(categorie_id)

        if categorie:
            for key, value in data.items():
                setattr(categorie, key, value)
        else:
            categorie = CategorieModel(**data)

        try:
            db.session.add(categorie)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return categorie