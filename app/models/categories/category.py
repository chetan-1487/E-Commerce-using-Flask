from app.extension import db
from datetime import datetime


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))

    createdAt = db.Column(db.DateTime, default=datetime.now())
    updatedAt = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now)

    products = db.relationship("Product", backref="category", lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description