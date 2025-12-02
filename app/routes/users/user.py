from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    make_response,
    url_for,
    flash,
    jsonify,
)
from app.forms.users import userForm, loginForm, forgotPassword
from app.models.users import User
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

def role_require(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user = get_jwt()
            role = [user.get("roles", [])]
            if not any(r in roles for r in role):
                resp = redirect(url_for("users.login"))
                unset_access_cookies(resp)
                unset_refresh_cookies(resp)
                flash("Permission denied. only admin can access")
                return resp
            return fn(*args,**kwargs)
        return decorator
    return wrapper



@user_bp.route("/")
def main():
    return redirect(url_for("users.signup"))


@user_bp.route("/signup", methods=["GET", "POST"])
def signup():
    user = userForm()

    if request.method == "POST" and user.validate_on_submit():

        username = user.username.data
        email = user.email.data
        password = user.password.data
        gender = user.gender.data
        address = user.address.data
        mobile_no = user.mobile_no.data
        roles = ",".join(user.role.data)

        userCheck = User.query.filter_by(email=email).first()
        if userCheck:
            flash("user already exist")
            return render_template("signup.html", form=user)

        if not is_valid_username(username):
            flash("username must be alphanumeric..")
            return render_template("signup.html", form=user)

        if not is_valid_password(password):
            flash(
                "password must have one lowercase, one uppercase, one digit, one special_character, length of 8"
            )
            return render_template("signup.html", form=user)

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        userDetail = User(
            username, email, password_hash, gender, address, mobile_no, roles
        )
        db.session.add(userDetail)
        db.session.commit()

        flash("Account created successfully!")
        return redirect(
            url_for("users.login")
        )  # it is used to avoid duplicate form submission

    return render_template("signup.html", form=user)


@user_bp.route("/login", methods=["GET", "POST"])
def login():

    login_form = loginForm()

    if request.method == "POST":

        email = login_form.email.data
        password = login_form.password.data

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("user doesn't exist.")
            return redirect(url_for("users.signup"))

        if bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(
                identity=str(user.id), additional_claims={"email": user.email, "roles": user.role}
            )
            refresh_token = create_refresh_token(
                identity=str(user.id), additional_claims={"email": user.email}
            )

            # response = make_response(redirect(url_for(f"{category_bp.name}.category")))
            response = make_response(redirect(url_for("users.all")))
            response.set_cookie(
                "access_token_cookie", access_token, httponly=True, samesite="Lax"
            )

            response.set_cookie(
                "refresh_token_cookie", refresh_token, httponly=True, samesite="Lax"
            )

            return response

        else:
            flash("Incorrect email or password")
            return render_template("login.html", form=login_form)
    return render_template("login.html", form=login_form)


@user_bp.route("/refresh-token")
@jwt_required(refresh=True)
def refreshToken():
    claims = get_jwt()
    email = claims.get("email")
    id = get_jwt_identity()
    new_token = create_access_token(identity=id, additional_claims={"email": email})
    new_res= make_response(url_for("users.all"))
    new_res.set_cookie(
        "access_token_cookie",
        new_token,
        httponly=True,
        samesite="Lax"
    )
    return new_res


@user_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    forgot_form = forgotPassword()

    if request.method == "POST":

        email = forgot_form.email.data
        current_password = forgot_form.current_password.data
        new_password = forgot_form.new_password.data
        confirm_password = forgot_form.confirm_password.data

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User doesnot exist..")
            return redirect(url_for("users.signup"))

        if bcrypt.check_password_hash(user.password, current_password):

            if new_password == confirm_password:

                if not is_valid_password(confirm_password):
                    flash(
                        "password must have one lowercase, one uppercase, one digit, one special_character, length of 8"
                    )
                    return render_template("signup.html", form=user)

                has_pass = bcrypt.generate_password_hash(confirm_password).decode(
                    "utf-8"
                )
                user.password = has_pass
                db.session.commit()

                flash("new password generated successfully..")
                return redirect(url_for("users.login"))

            flash("new password and confirm password doesnot match")
            return render_template("forgot.html", form=forgot_form)

    return render_template("forgot.html", form=forgot_form)


@user_bp.route("/logout")
def logout():
    response = make_response(redirect(url_for("users.login")))
    response.delete_cookie("access_token_cookie")
    response.delete_cookie("refresh_token_cookie")
    # unset_access_cookies(response)
    # unset_refresh_cookies(response)
    return response

@user_bp.route("/all", methods=["GET"])
@role_require("admin")
def all():
    users = User.query.all()

    return render_template("result.html", form=users)

