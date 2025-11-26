from app.extension import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    image_url = db.Column(db.String(100), nullable=True)

    createdAt = db.Column(db.DateTime, default=datetime.now())
    updatedAt = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __init__(self, name, description, price, stock, category_id):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category_id = category_id
