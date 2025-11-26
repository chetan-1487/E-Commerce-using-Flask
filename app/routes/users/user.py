from flask import Blueprint, render_template, redirect, request, make_response, url_for, Response, flash
from app.forms.users import userForm, loginForm, forgotPassword, resetPassword
from app.models.users import User
from app.extension import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_manager, unset_access_cookies

user_bp = Blueprint("users",__name__,template_folder=".../templates",static_folder=".../static")

@user_bp.route("/")
def main():
  return redirect(url_for("users.signup"))

@user_bp.route("/signup", methods=["GET","POST"])
def signup():
  user = userForm()

  if request.method=="POST" and user.validate_on_submit():
      
    username = user.username.data
    email = user.email.data
    password = user.password.data
    gender = user.gender.data
    address = user.address.data
    mobile_no = user.mobile_no.data
    role = user.role.data

    userCheck = User.query.filter_by(email=email).first()
    if(userCheck):
      flash("user already exist")
      return render_template("signup.html", form=user)
      
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    userDetail = User(username, email, password_hash, gender, address, mobile_no, role)
    db.session.add(userDetail)
    db.session.commit()

    flash("Account created successfully! ", "success")
    return redirect(url_for("users.login")) # it is used to avoid duplicate form submission

  return render_template("signup.html", form=user)

@user_bp.route("/login", methods=["GET","POST"])
def login():

  login_form = loginForm()

  if request.method == "post":

    email = login_form.email.data
    password = login_form.password.data

    user = User.query.filter_by(email=email).first()

    if not user:
      flash("user doesn't exist.")
      return redirect(url_for("users.signup"))

    if bcrypt.check_password_hash(User.password, password):
      token = create_access_token(identity=str(User.id), additional_claims={"email":email})
      response = make_response(redirect("users.category"))
      response.set_cookie(
        "token",
        token,
        httponly=True,
        samesite="Latex"
      )
      return response
  return render_template("login.html")

@user_bp.route("/refresh-token")
def refresh_token():
  return "refresh token"

@user_bp.route("/forgot-password")
def forgot_password():
  return render_template("forgot.html")


@user_bp.route("/reset-password")
def reset_password():
  return render_template("reset.html")