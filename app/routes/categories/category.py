from flask import Blueprint, url_for, redirect, render_template, make_response
from app.models.products import Product


category_bp = Blueprint("categories", __name__, template_folder=".../templates", static_folder=".../static")

@category_bp.route("/products")
def products():
  return render_template("category.html")