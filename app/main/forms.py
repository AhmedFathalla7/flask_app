from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class CreateAuthorForm(FlaskForm):
    name = StringField('Author Name', validators=[DataRequired()])
    submit = SubmitField('Create Author')

class CreateBookForm(FlaskForm):
    name = StringField('Book Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    publish_date = DateField('Publish Date', format='%Y-%m-%d', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    age_group = SelectField(
        'Appropriate For', 
        choices=[('Under 8', 'Under 8'), ('8-15', '8-15'), ('Adults', 'Adults')], 
        validators=[DataRequired()]
    )
    author_id = SelectField('Author', coerce=int, validators=[DataRequired()])
    image = FileField('Book Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Create Book')

