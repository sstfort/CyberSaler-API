from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from db import db
from models.article import ArticleModel
from models.categorie import CategorieModel
from models.article import ArticleSchema

blp = Blueprint(
    "articles",
    __name__,
    description="Operations on articles"
)

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@blp.route("/article")
class ArticleListResource(MethodView):

    @jwt_required()
    @blp.response(200, ArticleSchema(many=True))
    def get(self):
        return ArticleModel.query.all()

    @jwt_required()
    @blp.arguments(ArticleSchema)
    @blp.response(201, ArticleSchema)
    def post(self, data):

        # ✅ FK validation
        if not CategorieModel.query.get(data["categorie_id"]):
            abort(400, message="Invalid categorie_id")

        # ✅ unique checks
        if ArticleModel.query.filter_by(article_code=data["article_code"]).first():
            abort(400, message="article_code already exists")

        if ArticleModel.query.filter_by(article_desc=data["article_desc"]).first():
            abort(400, message="article_desc already exists")

        article = ArticleModel(**data)

        try:
            db.session.add(article)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return article
    

@blp.route("/article/<int:article_id>")
class ArticleResource(MethodView):

    @jwt_required()
    @blp.response(200, ArticleSchema)
    def get(self, article_id):
        return ArticleModel.query.get_or_404(article_id)

    @jwt_required()
    def delete(self, article_id):
        article = ArticleModel.query.get_or_404(article_id)

        db.session.delete(article)
        db.session.commit()

        return {"message": "Article deleted"}, 200


    @jwt_required()
    @blp.arguments(ArticleSchema)
    @blp.response(200, ArticleSchema)
    def put(self, data, article_id):

        article = ArticleModel.query.get(article_id)

        # ✅ FK validation
        if "categorie_id" in data:
            if not CategorieModel.query.get(data["categorie_id"]):
                abort(400, message="Invalid categorie_id")

        if article:
            for key, value in data.items():
                setattr(article, key, value)
        else:
            article = ArticleModel(**data)

        try:
            db.session.add(article)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return article