from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class UserRegisterForm(FlaskForm):
    """User Form. Username and password"""

    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=20, message="Username needs to be between 5 and 20 characters")])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Length(min=6, max=50, message="Email needs to be between 6 and 50 characters")])
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=1, max=30, message="First Name needs to be between 1 and 30 characters")])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=1, max=30, message="Last Name needs to be between 1 and 30 characters")])

class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=20, message="Username needs to be between 5 and 20 characters")])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=100, message="Title needs to be less than 100 characters.")])
    content = StringField("Content", validators=[InputRequired()])

class EditFeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=100, message="Title needs to be less than 100 characters.")])
    content = StringField("Content", validators=[InputRequired()])