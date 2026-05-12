from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from db import db

from models.level import LevelModel
from models.level import LevelSchema


blp = Blueprint(
    "levels",
    __name__,
    description="Operations on levels"
)


@blp.route("/level")
class LevelListResource(MethodView):

    @jwt_required()
    @blp.response(200, LevelSchema(many=True))
    def get(self):
        return LevelModel.query.all()

    @jwt_required()
    @blp.arguments(LevelSchema)
    @blp.response(201, LevelSchema)
    def post(self, data):

        exists = LevelModel.query.get(
            data["level_id"]
        )

        if exists:
            abort(
                400,
                message="level_id already exists"
            )

        level = LevelModel(**data)

        try:
            db.session.add(level)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return level


@blp.route("/level/<int:level_id>")
class LevelResource(MethodView):

    @jwt_required()
    @blp.response(200, LevelSchema)
    def get(self, level_id):
        return LevelModel.query.get_or_404(level_id)

    @jwt_required()
    def delete(self, level_id):

        level = LevelModel.query.get_or_404(level_id)

        db.session.delete(level)
        db.session.commit()

        return {
            "message": "Level deleted"
        }, 200

    @jwt_required()
    @blp.arguments(LevelSchema)
    @blp.response(200, LevelSchema)
    def put(self, data, level_id):

        level = LevelModel.query.get(level_id)

        if level:
            level.level_name = data["level_name"]
        else:
            level = LevelModel(**data)

        try:
            db.session.add(level)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return level