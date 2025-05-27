from wtforms import Form, StringField, SubmitField, validators

class ExtractionForm(Form):
    product_id = StringField("Product_id", name="product_id", id="product_id", validators=[
        validators.DataRequired(message="Product ID is required"),
        validators.Length(min=6, max=11, message="Product ID should have between 6 and 11 characters"),
        validators.Regexp(r"[0-9]+$",message="Product ID can contain only digits")
    ])
    submit = SubmitField("Extract opinions")