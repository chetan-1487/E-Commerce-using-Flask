from flask import Blueprint, url_for, redirect, render_template, make_response
from app.models.products import Product


product_bp = Blueprint("products", __name__, template_folder=".../templates", static_folder=".../static")

@product_bp.route("/products")
def products():
  return render_template("products.html")