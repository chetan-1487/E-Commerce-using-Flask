from flask import Flask
from flask_cors import CORS
from app.routes.users import user_bp
from app.config import Config
from app.extension import jwt, db, migrate, limiter
from app.routes.categories import category_bp
from app.routes.products import product_bp

from app.models.categories.category import Category
from app.models.products.product import Product

def createApp(test_config=None, testing=False) -> Flask:

    app = Flask(__name__)

    app.config.from_object(Config)

    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:chetan@localhost:5432/test"

    CORS(app, resources={r"/*":{"origins":"*"}})

    limiter.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)

    return app


if __name__ == "__main__":
    app = createApp()
    app.run(debug=True)
