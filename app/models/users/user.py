from app.extension import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    mobile_no = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(100), default="user")

    createdAt = db.Column(db.DateTime, default=datetime.now())

    def __init__(
        self, username, email, password, gender, address, mobile_no, role="user"
    ):
        self.username = username
        self.email = email
        self.password = password
        self.gender = gender
        self.address = address
        self.mobile_no = mobile_no
        self.role = role

    def __repr__(self):
        return f"username --> {self.username}"
