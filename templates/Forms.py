from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators,ValidationError
from wtforms.fields import EmailField, DateField



class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
    address = TextAreaField('Home Address', [validators.length(max=200), validators.DataRequired()])
    membership = RadioField('Preferences', choices=[('B', 'Vegetarian'), ('S', 'Vegan'), ('G', 'None')], default='F')
    remarks = TextAreaField('Remarks', [validators.Optional()])

    def validate_first_name(form,first_name):
        if not form.first_name.data.isalpha():
            raise ValidationError("First Name shouldnt contain digits")

    def validate_last_name(form,last_name):
        if not form.last_name.data.isalpha():
            raise ValidationError("Last Name shouldnt contain digits")

