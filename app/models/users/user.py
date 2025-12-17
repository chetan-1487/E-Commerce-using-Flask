from app.extension import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum
from sqlalchemy import Enum as postgreenum

class Gender(Enum):
    Male = "Male"
    Female = "Female"
    Others = "Others"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(postgreenum(Gender), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    mobile_no = db.Column(db.String(10), nullable=False)
    role = db.Column(ARRAY(db.String), default="user")

    createdAt = db.Column(db.DateTime, default=datetime.now())

    def __init__(
        self, username, email, password, gender, address, mobile_no, role
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
