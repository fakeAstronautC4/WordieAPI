from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired, ValidationError

#This function prevents the user from using spaces in the string
def no_spaces(form, field):
    if ' ' in field.data:
        raise ValidationError('Input cannot contain spaces')


class WordForm(FlaskForm):
    word = StringField("Enter a word: ", validators=[DataRequired(), Length(max=20), no_spaces])