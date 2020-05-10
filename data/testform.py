from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TestForm(FlaskForm):
    password = StringField('Введите пароль', validators=[DataRequired()])
    submit = SubmitField('Проверить')
