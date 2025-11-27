from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class categoryForm(FlaskForm):
    name = StringField(
        "Category Name", [validators.data_required("Please enter product category")]
    )
    description = StringField("Category desc")
    submit = SubmitField("Submit")
