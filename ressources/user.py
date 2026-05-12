from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256


from utils.getenv import getenv
import requests

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from passlib.hash import sha256_crypt # pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import g, request

from db import db
from blocklist import BLOCKLIST

from models.user import UserModel
from models.entreprise import EntrepriseModel
from models.distribution import DistributionModel

from models.user import UserSchema, UserLoginSchema, UserChangePwdSchema


blp = Blueprint(
    "users",
    __name__,
    description="Operations on users"
)


@blp.route("/user")
class UserListResource(MethodView):

    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    #@jwt_required()
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, data):

        # ✅ unique username
        if UserModel.query.filter_by(
            username=data["username"]
        ).first():
            abort(400, message="username already exists")

        # ✅ FK validation
        if (
            data.get("entreprise_id")
            and not EntrepriseModel.query.get(
                data["entreprise_id"]
            )
        ):
            abort(400, message="Invalid entreprise_id")

        if (
            data.get("distribution_id")
            and not DistributionModel.query.get(
                data["distribution_id"]
            )
        ):
            abort(400, message="Invalid distribution_id")

        # ✅ password hash
        data["password"] = pbkdf2_sha256.hash(
            data["password"]
        )

        user = UserModel(**data)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return user



@blp.route("/user/<int:user_id>")
class UserResource(MethodView):

    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        return UserModel.query.get_or_404(user_id)

    @jwt_required()
    def delete(self, user_id):

        user = UserModel.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted"}, 200

    @jwt_required()
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, data, user_id):

        user = UserModel.query.get(user_id)

        # ✅ unique username
        exists = UserModel.query.filter(
            UserModel.username == data["username"],
            UserModel.user_id != user_id
        ).first()

        if exists:
            abort(400, message="username already exists")

        # ✅ FK validation
        if (
            data.get("entreprise_id")
            and not EntrepriseModel.query.get(
                data["entreprise_id"]
            )
        ):
            abort(400, message="Invalid entreprise_id")

        if (
            data.get("distribution_id")
            and not DistributionModel.query.get(
                data["distribution_id"]
            )
        ):
            abort(400, message="Invalid distribution_id")

        # ✅ password hash
        data["password"] = pbkdf2_sha256.hash(
            data["password"]
        )

        if user:
            for key, value in data.items():
                setattr(user, key, value)
        else:
            user = UserModel(**data)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return user



def get_seconds_until_midnight():
    """Calculate the number of seconds remaining until midnight."""
    now = datetime.utcnow()
    midnight = datetime.combine(now.date(), datetime.min.time()) + timedelta(days=1)  # Next midnight
    return (midnight - now).seconds  # Difference in seconds




@blp.route("/user/login")
class UserLoginResource(MethodView):

    @blp.arguments(UserLoginSchema)
    def post(self, user_data):

        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and user.statut_user == 0:
            abort(
                403,
                message="Utilisateur desactivé. Merci de contacter votre administrateur."
            )

        if user and pbkdf2_sha256.verify(
            user_data["password"],
            user.password
        ):

            expires_in = timedelta(
                seconds=get_seconds_until_midnight()
            )

            access_token = create_access_token(
                identity=str(user.user_id),
                fresh=True,
                expires_delta=expires_in,
                additional_claims={
                    "user_id": user.user_id,
                    "username": user.username,
                    "nom_prenom": user.nom_prenom,
                    "entreprise_id": user.entreprise_id,
                    "distribution_id": user.distribution_id,
                    "level_id": user.level_id,
                    "statut_user": user.statut_user
                }
            )

            refresh_token = create_refresh_token(
                identity=str(user.user_id)
            )

            user.connected = 1

            db.session.commit()

            return {
                "id": user.user_id,
                "user": user.username,
                "access_token": access_token,
                "refresh_token": refresh_token
            }

        abort(
            403,
            message="Informations d'identification non valides."
        )


@blp.route("/user/logout")
class UserLogout(MethodView):
    @jwt_required()
    def get(self):
         
        jwt = get_jwt()
        
        # logout on kolos
        # Retrieve headers
        kolos_token = request.headers.get('Kolos-Token')
        # url for logout
        url = f"{getenv()['BASE_URL_KOLOS']}/user/logout"
        headers = {"Authorization": f"Bearer {kolos_token}"}
        data = {
            "username": jwt['numero_compte']
        } 
        response = requests.post(url=url, json=data, headers=headers)

        # logout on cyberlotto
        BLOCKLIST.add(jwt["jti"])

        return {"message": "Successfully logged out."}



@blp.route("/user/chgpwd")
class UserChgPwd(MethodView):
    @jwt_required()
    @blp.arguments(UserChangePwdSchema)
    def put(self, user_data):
        jwt = get_jwt()
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        
        if not user:
            abort(403, message="This account does not exist.")

        if jwt.get("user_id") != str(user.user_id):
            abort(403, message="Please assume the username before continuing.")
        
        if user and user.statut_user == 0:
            abort(403, message="User deactivated. Please contact your administrator.")

        if user and sha256_crypt.verify(user_data["old_password"], user.password):
            if user_data["new_password"] == user_data["confirm_password"]:
                user.password = sha256_crypt.hash(user_data["confirm_password"])
                user.first_auth = 0
                user.modifie_par = jwt.get('user_id')
                db.session.commit()
                db.session.close()

                current_user = get_jwt_identity()
                new_token = create_access_token(identity=current_user, fresh=False)
                return {"message": "Password changed successfully."}
            else:
                abort(403, message="Merci de confirmer le nouveau mot-de-passe.")
        else:      
            abort(403, message="Ancien mot-de-passe incorrect. Merci de réesseyer.")