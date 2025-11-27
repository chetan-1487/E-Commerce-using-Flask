from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField,
    EmailField,
    PasswordField,
    RadioField,
    validators,
    SelectField,
    SubmitField,
    StringField,
    SelectMultipleField,
)


class userForm(FlaskForm):
    username = StringField(
        "Username", [validators.DataRequired("please enter your username")]
    )
    email = EmailField(
        "Email",
        [
            validators.DataRequired("Please enter your email."),
            validators.Email("Please enter your email."),
        ],
    )
    password = PasswordField(
        "Password", [validators.DataRequired("Please enter password")]
    )
    gender = RadioField(
        "Gender", choices=[("M", "MALE"), ("F", "FEMALE"), ("O", "OTHERS")]
    )
    address = TextAreaField(
        "Address", [validators.DataRequired("Address is required.")]
    )
    mobile_no = StringField(
        "Mobile_no", [validators.DataRequired("mobile no is required.")]
    )
    role = SelectMultipleField("Role", choices=[("user", "User"), ("admin", "Admin")])
    submit = SubmitField("Signup")


class loginForm(FlaskForm):
    email = EmailField("Email", [validators.DataRequired("Please enter your email")])
    password = PasswordField(
        "Password", [validators.DataRequired("Please enter password")]
    )
    submit = SubmitField("Login")


class forgotPassword(FlaskForm):
    email = EmailField("Email", [validators.DataRequired("Please enter your email")])
    current_password = PasswordField(
        "Current Password", [validators.DataRequired("Current passwrd in required")]
    )
    new_password = PasswordField(
        "New Password", [validators.DataRequired("New passwrd in required")]
    )
    confirm_password = PasswordField(
        "Confirm Password", [validators.DataRequired("Confirm passwrd in required")]
    )
    submit = SubmitField("Submit")
