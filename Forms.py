from wtforms import Form, RadioField, TextAreaField, validators


class FeedbackForm(Form):
    rating = RadioField("Rating", choices=[("VB", "Very Bad"), ("B", "Bad"), ("N", "Neutral"), ("G", "Good"), ("VG", "Very Good")], default="VG")
    remarks = TextAreaField("Remarks", [validators.Optional()])
