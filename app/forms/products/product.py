from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField, IntegerField, URLField


class Product(FlaskForm):
  name = StringField("Name", [validators.DataRequired("Product name is required.")])
  description = TextAreaField("Description")
  price = IntegerField("Price",[validators.DataRequired("Price is required.")])
  stock = IntegerField("Stock",[validators.DataRequired("Stock must be mention.")])
  image_url = URLField("Image_url")
  submit = SubmitField("Submit")