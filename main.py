from flask import Flask, render_template, redirect, request, make_response, session
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'



def main():
    db_session.global_init("db/manager.sqlite")

    @app.route("/")
    def index():
        session = db_session.create_session()
        return render_template("index.html")

    class RegisterForm(FlaskForm):
        email = EmailField('Почта', validators=[DataRequired()])
        password = PasswordField('Пароль', validators=[DataRequired()])
        password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
        name = StringField('Имя пользователя', validators=[DataRequired()])
        submit = SubmitField('Войти')

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                email=form.email.data,
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)

    @app.route("/genpass")
    def genpass():
        session = db_session.create_session()
        return render_template("genpass.html")

    @app.route("/testpass")
    def testpass():
        session = db_session.create_session()
        return render_template("testpass.html")

    @app.route("/manager")
    def manager():
        session = db_session.create_session()
        return render_template("manager.html")

    app.run()


if __name__ == '__main__':
    main()
