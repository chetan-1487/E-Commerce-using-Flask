from flask import Flask
from app.routes.users import user_bp
from app.config import Config
from app.extension import jwt, db, migrate
from app.routes.categories import category_bp
from app.routes.products import product_bp

from app.models.categories.category import Category
from app.models.products.product import Product

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(category_bp)
app.register_blueprint(product_bp)


if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(debug=True)
