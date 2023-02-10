from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, PasswordField, validators, ValidationError
from wtforms.fields import EmailField, DateField
from email_validator import validate_email, EmailNotValidError


#Nicholas
class FeedbackForm(Form):
    rating = RadioField("Rating", choices=[("VB", "Very Bad"), ("B", "Bad"), ("N", "Neutral"), ("G", "Good"), ("VG", "Very Good")], default="VG")
    remarks = TextAreaField("Remarks", [validators.Optional()])


#Nicholas
class LoginForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


#Nicholas
class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
    address = TextAreaField('Home Address', [validators.length(max=200), validators.DataRequired()])
    membership = RadioField('Membership', choices=[('B', 'Bronze'), ('S', 'Silver'), ('G', 'Gold')], default='F')
    remarks = TextAreaField('Remarks', [validators.Optional()])
    password = StringField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])

    def validate_first_name(form, first_name):
        if not form.first_name.data.isalpha():
            raise ValidationError("First Name shouldn't contain digits")

    def validate_last_name(form, last_name):
        if not form.last_name.data.isalpha():
            raise ValidationError("Last Name shouldn't contain digits")
