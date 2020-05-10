from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class DeleteForm(FlaskForm):
    url = StringField('Введите URL', validators=[DataRequired()])
    login = StringField('Введите логин', validators=[DataRequired()])
    submit = SubmitField('Удалить')
