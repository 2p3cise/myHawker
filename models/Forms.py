from wtforms import Form, StringField, validators, SubmitField, IntegerField, DateField, DecimalField, TextAreaField, \
    SelectField, ValidationError, RadioField, EmailField, PasswordField, FileField


class CreateVoucherForm(Form):
    code = StringField('Code', [validators.Length(min=1, max=10), validators.DataRequired()])
    discount = IntegerField('Discount', [validators.NumberRange(min=1, max=100), validators.DataRequired()])
    expiry_date = DateField('Expiry Date', format='%Y-%m-%d')

    submit = SubmitField("Add Coupon")


# ----------------------------------------------------------Sharvin's code---------------------------------------------------------------------------
class CreateDishForm(Form):
    dish_name = StringField('Dish Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.Length(min=10, max=1024), validators.DataRequired()])
    cuisine = SelectField("Select Cuisine", [validators.DataRequired('Please choose a cuisine!')],
                          choices=[("", 'Select a Cuisine'), ("indian", 'Indian Cuisine'),
                                   ("western", 'Western Cuisine'), ("mixedrice", 'Mixed Rice'),
                                   ("ayampenyet", 'Ayam Penyet')])
    image = FileField("Product Image", validators=[])

    def validate_price(form, price):
        if form.price.data < 0:
            raise ValidationError("Cannot input negative numbers!")


# Nicholas
class FeedbackForm(Form):
    rating = RadioField("Rating", choices=[("VB", "Very Bad"), ("B", "Bad"), ("N", "Neutral"), ("G", "Good"),
                                           ("VG", "Very Good")], default="VG")
    remarks = TextAreaField("Remarks", [validators.Optional()])


# Nicholas
class LoginForm(Form):
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


# Nicholas
class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
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
