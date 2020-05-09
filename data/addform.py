from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    url = StringField('Введите URL', validators=[DataRequired()])
    login = StringField('Введите логин', validators=[DataRequired()])
    password = StringField(' Введите пароль', validators=[DataRequired()])
    submit = SubmitField('Добавить')
