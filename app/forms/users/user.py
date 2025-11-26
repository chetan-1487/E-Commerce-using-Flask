from flask_wtf import FlaskForm
from wtforms import TextAreaField, EmailField, PasswordField, RadioField, validators, SelectField, SubmitField, StringField

class userForm(FlaskForm):
  username = StringField("Username",[validators.DataRequired("please enter your username")])
  email = EmailField("Email", [validators.DataRequired("Please enter your email."), validators.Email("Please enter your email.")])
  password = PasswordField("Password", [validators.DataRequired("Please enter password")])
  gender = RadioField("Gender", choices=[("M","MALE"), ("F","FEMALE"), ("O","OTHERS")])
  address = TextAreaField("Address", [validators.DataRequired("Address is required.")])
  mobile_no = StringField("Mobile_no", [validators.DataRequired("mobile no is required.")])
  role = SelectField("Role", choices = [('user', 'User'), ('admin', 'Admin')])
  submit = SubmitField("Signup")

class loginForm(FlaskForm):
  email = EmailField("Email", [validators.DataRequired("Please enter your email")])
  password = PasswordField("Password", [validators.DataRequired("Please enter password")])
  submit = SubmitField("Login")

class forgotPassword(FlaskForm):
  email = EmailField("Email", [validators.DataRequired("Please enter your email")])
  submit = SubmitField("Submit")

class resetPassword(FlaskForm):
  email = EmailField("Email", [validators.DataRequired("Please enter your email")])
  password = PasswordField("Password", [validators.DataRequired("Please enter new password")])
  submit = SubmitField("Submit")