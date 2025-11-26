from flask import Blueprint, render_template, redirect, request, make_response, url_for, Response, flash, jsonify
from app.forms.users import userForm, loginForm, forgotPassword, resetPassword
from app.models.users import User
from app.extension import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, unset_access_cookies, create_refresh_token, get_jwt_identity, get_jwt
from app.utils import is_valid_password, is_valid_username, generateOtp

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
    
    if not is_valid_username(username):
      flash("username must be alphanumeric..")
      return render_template("signup.html", form=user)
    
    if not is_valid_password(password):
      flash("password must have one lowercase, one uppercase, one digit, one special_character, length of 8")
      return render_template("signup.html", form=user)

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    userDetail = User(username, email, password_hash, gender, address, mobile_no, role)
    db.session.add(userDetail)
    db.session.commit()

    flash("Account created successfully!")
    return redirect(url_for("users.login")) # it is used to avoid duplicate form submission

  return render_template("signup.html", form=user)

@user_bp.route("/login", methods=["GET","POST"])
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
      access_token = create_access_token(identity=str(user.id), additional_claims={"email":user.email})
      refresh_token=  create_refresh_token(identity=str(user.id), additional_claims={"email":user.email})
      
      response = make_response(redirect(url_for("users.category")))
      response.set_cookie(
        "access_token_cookie",
        access_token,
        httponly=True,
        samesite="Lax"
      )

      response.set_cookie(
        "refresh_token_cookie",
        refresh_token,
        httponly=True,
        samesite="Lax"
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
  new_token = create_access_token(identity=id, additional_claims={"email":email})
  return jsonify({"new_token":new_token})

@user_bp.route("/forgot-password")
def forgot_password():
  
  return render_template("forgot.html")


@user_bp.route("/reset-password")
def reset_password():
  return render_template("reset.html")

@user_bp.route("/logout")
def logout():
  response=make_response(redirect(url_for("users.login")))
  unset_access_cookies(response)
  return response

@user_bp.route("/category")
def category():
  return render_template("category.html")