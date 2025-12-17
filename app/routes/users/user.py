from flask import (
    Blueprint,
    request,
    make_response,
    jsonify
)
from flask.wrappers import Response
from app.extension import limiter
from app.models.users import User, Gender
from app.extension import db, bcrypt
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    unset_access_cookies,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    unset_refresh_cookies,
    verify_jwt_in_request
)
from app.utils import is_valid_password, is_valid_username
from app.routes.categories import category_bp
from functools import wraps

user_bp = Blueprint(
    "users", __name__, template_folder=".../templates", static_folder=".../static"
)

ROLE_PERMISSION={
    "admin":["signup","update","delete"],
    "user":["all"]
}

def permission(*roles):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            verify_jwt_in_request(locations=["headers","cookies"])
            user = get_jwt()
            role = user.get(roles, [])

            permission = ROLE_PERMISSION.get(role)
            if roles not in permission:
                return jsonify({"message":"only admin can create, update adn delete users"})
            return func(*args,**kwargs)
        return decorator
    return wrapper



def role_require(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request(locations=["headers", "cookies"])
            user = get_jwt()
            role = user.get("roles", [])
            if not any(r in roles for r in role):
                resp = make_response(jsonify({"message":"permission denied, only admin take action"}))
                unset_access_cookies(resp)
                unset_refresh_cookies(resp)
                return resp
            return fn(*args,**kwargs)
        return decorator
    return wrapper



@user_bp.route("/")
def main():
    return jsonify({"message":"App is running"})


@user_bp.route("/signup", methods=["POST"])
def signup() -> Response:

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    gender = data.get("gender")
    address = data.get("address")
    mobile_no = data.get("mobile_no")
    roles = data.get("role", [])

    try:
        Gender(gender)
    except ValueError:
        return jsonify({"message":"gender value should be Male, Female and Others"})

    userCheck = User.query.filter_by(email=email).first()
    if userCheck:
        return jsonify({"message":"user already exist."}), 200

    if not is_valid_username(username):
        return jsonify({"message":"username must be alphanumeric.."})

    if not is_valid_password(password):
        return jsonify({"message":"password must have one lowercase, one uppercase, one digit, one special_character, length of 8"}),200

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    userDetail = User(
        username, email, password_hash, gender, address, mobile_no, roles
    )
    db.session.add(userDetail)
    db.session.commit()

    return jsonify({
    "message": "User account created successfully.",
    "user": {
        "username": username,
        "email": email,
        "gender": gender,
        "address": address,
        "mobile_no": mobile_no,
        "roles": roles,
        "createdAt": userDetail.createdAt
        }
    }), 200



@user_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login() -> Response:

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message":"user not exist"})

    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(
            identity=str(user.id), additional_claims={"email": user.email, "roles": user.role}
        )
        refresh_token = create_refresh_token(
            identity=str(user.id), additional_claims={"email": user.email}
        )

        response = make_response(
        jsonify({
            "message": "Login successful",
            "tokens":{
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role
                }
            }), 200
        )
        
        response.set_cookie(
            "access_token_cookie", access_token, httponly=True, samesite="Lax"
        )

        response.set_cookie(
            "refresh_token_cookie", refresh_token, httponly=True, samesite="Lax"
        )

        return response
    else:
        return jsonify({"message":"email and password is incorrect."})


@user_bp.route("/refresh-token")
@jwt_required(refresh=True)
def refreshToken() -> Response:
    claims = get_jwt()
    email = claims.get("email")
    id = get_jwt_identity()
    new_token = create_access_token(identity=id, additional_claims={"email": email})
    new_res= make_response(jsonify({"message":"new token is generated sucessfully","access token": new_token}),200)
    new_res.set_cookie(
        "access_token_cookie",
        new_token,
        httponly=True,
        samesite="Lax"
    )
    return new_res


@user_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password() ->Response:

    data = request.get_json()
    email = data.get("email")
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message":"email doesnot exist."})

    if bcrypt.check_password_hash(user.password, current_password):

        if new_password == confirm_password:

            if not is_valid_password(confirm_password):
                return jsonify({"message":"password must have one lowercase, one uppercase, one digit, one special_character, length of 8"})

            has_pass = bcrypt.generate_password_hash(confirm_password).decode(
                "utf-8"
            )
            user.password = has_pass
            db.session.commit()

            return jsonify({"message":"new password is generated successfully"}),200
        else:
            return jsonify({"message":"new and confirm password mismatch."})
    else:
        return jsonify({"message":"email and password is incorrect."})



@user_bp.route("/logout")
def logout()->Response:
    response = make_response(jsonify({"message":"logout successfully"}))
    response.delete_cookie("access_token_cookie")
    response.delete_cookie("refresh_token_cookie")

    return response

@user_bp.route("/all", methods=["GET"])
@role_require("admin")
def all() -> Response:
    users = User.query.all()

    users_list = [
        {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "gender": user.gender,
            "address":user.address,
            "mobile_no":user.mobile_no,
            "created_at": user.createdAt if user.createdAt else None
        }
        for user in users
    ]

    return jsonify({
        "total": len(users_list),
        "users": users_list
    })


@user_bp.route("/update/<int:id>", methods=["PUT"])
@permission("admin")
def update(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body is required"}), 400

    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({"error": "Hotel record not found"}), 404

    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.session.commit()

    return jsonify({
        "message": "Update successful",
        "updated_id": id,
        "updated_data": data
    }), 200

