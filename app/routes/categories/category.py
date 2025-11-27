from flask import Blueprint, url_for, redirect, render_template, make_response, request, flash
from app.models.products import Product
from app.forms.categories import categoryForm
from app.models.categories import Category
from app.extension import db


category_bp = Blueprint("categories", __name__, template_folder=".../templates", static_folder=".../static")

@category_bp.route("/category")
def category():
  return render_template("category.html")

@category_bp.route("/create", methods=["GET","POST"])
def create():

  form = categoryForm()

  if request.method=="POST":

    name = form.name.data
    desc = form.description.data

    category_detail = Category(name, desc)
    db.session.add(category_detail)
    db.session.commit()

    flash("Category created successfully..")
    return render_template("allCategory.html", form=form)
  
  return render_template("allCategory.html", form=form)
