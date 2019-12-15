
from flask_wtf import FlaskForm
from wtforms.fields import SelectField, TextAreaField, SubmitField, StringField, PasswordField, IntegerField, FileField, FloatField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired


# creates the login form
class LoginForm(FlaskForm):
    name = StringField("User Name", validators=[
        InputRequired('Enter user name')])
    password_hash = PasswordField("Password", validators=[
        InputRequired('Enter user password')])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):  # creates the register form
    name = StringField("User Name", validators=[
                       InputRequired('Enter a Name')])
    emailid = StringField('Email Address', validators=[
                          InputRequired('Enter an Email'), Email()])

    phone = IntegerField('Phone Number', validators=[
                         InputRequired('Please enter a Phone Number'), NumberRange(min=100000000, max=9999999999, message="Please enter a valid 10 digit long phone number")])

    location = StringField("Address", validators=[
                           InputRequired('Please enter an address')])

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired('Please enter a password'),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")


ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}

#Item creation form
class CreationForm(FlaskForm):  # creates the item upload form
    name = StringField("Item Title", validators=[
                       InputRequired('Enter a Name')])
    model = StringField("Item model", validators=[
        InputRequired('Enter a model name')])
    price = FloatField('Price', validators=[
        InputRequired('Please enter valid Price')])
    category = SelectField("Category", choices=[(
        'CPU', 'CPU'), ('GPU', 'GPU'), ('Case', 'Case'), ('Memory', 'Memory'), ('Motherboard', 'Motherboard'), ('CPU Cooler', 'CPU Cooler'), ('Storage', 'Storage'), ('Peripherals', 'Peripherals'), ('Power Supply', 'Power Supply')])
    description = TextAreaField("Description", validators=[
        InputRequired('Enter a Name')])
    quality = SelectField("Quality", choices=[(
        'New', 'New'), ('Used/Excelent', 'Used/Excelent'), ('Used/Good', 'Used/Good'), ('Used/Moderate', 'Used/Moderate'), ('Used/Needs Repairs5', 'Used/Needs Repairs')])
    image = FileField("Product Image:", validators=[FileRequired(message='Image can not be empty'),
                                                    FileAllowed(ALLOWED_FILE, message='Only support png, jpg, JPG, PNG, bmp')])
    submit = SubmitField("Post Item")

#item edit form
class EditForm(FlaskForm):
    name = StringField("Item Title", validators=[
                       InputRequired('Enter a Name')])
    model = StringField("Item model", validators=[
        InputRequired('Enter a model name')])
    price = FloatField('Price', validators=[
        InputRequired('Please enter valid Price')])
    category = SelectField("Category", choices=[(
        'CPU', 'CPU'), ('GPU', 'GPU'), ('Case', 'Case'), ('Memory', 'Memory'), ('Motherboard', 'Motherboard'), ('CPU Cooler', 'CPU Cooler'), ('Storage', 'Storage'), ('Peripherals', 'Peripherals'), ('Power Supply', 'Power Supply')])
    description = TextAreaField("Description", validators=[
        InputRequired('Enter a Name')])
    quality = SelectField("Quality", choices=[(
        'New', 'New'), ('Used/Excelent', 'Used/Excelent'), ('Used/Good', 'Used/Good'), ('Used/Moderate', 'Used/Moderate'), ('Used/Needs Repairs5', 'Used/Needs Repairs')])
    image = FileField("Product Image:", validators=[FileAllowed(
        ALLOWED_FILE, message='Only support png, jpg, JPG, PNG, bmp')])
    submit = SubmitField("Edit")


class searchForm(FlaskForm):  # creates the form for the search field
    category = SelectField("Category", choices=[(
        'CPU', 'CPU'), ('GPU', 'GPU'), ('Case', 'Case'), ('Memory', 'Memory'), ('Motherboard', 'Motherboard'), ('CPU Cooler', 'CPU Cooler'), ('Storage', 'Storage'), ('Peripherals', 'Peripherals'), ('Power Supply', 'Power Supply')])
    submit = SubmitField("Search")


class bidForm(FlaskForm):  # creates the form for the bid button
    submit = SubmitField("Yes")
