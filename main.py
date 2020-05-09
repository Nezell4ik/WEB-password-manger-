from flask import Flask, render_template, redirect, request, make_response, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session, passwords
from data.addform import AddForm
from data.loginform import LoginForm
from data.passwords import Password
from data.registerform import RegisterForm
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/manager.sqlite")

    @app.route("/")
    def index():
        session = db_session.create_session()
        return render_template("index.html")

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

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            user = session.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

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
        if current_user.is_authenticated:
            session = db_session.create_session()
            passwords = session.query(Password).filter(Password.user == current_user)
            return render_template("manager.html", passwords=passwords)
        else:
            session = db_session.create_session()
            return render_template("manager.html")

    @app.route('/add', methods=['GET', 'POST'])
    def add():
        form = AddForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            passwords = Password()
            passwords.url = form.url.data
            passwords.login = form.login.data
            passwords.password = form.password.data
            current_user.passwords.append(passwords)
            session.merge(current_user)
            session.commit()
            return redirect('/manager')
        return render_template('addordel.html', title='добавление пароля', form=form)

    @app.route('/change')
    def change():
        session = db_session.create_session()
        return render_template("addordel.html")

    @app.route('/delete')
    def delete():
        session = db_session.create_session()
        return render_template("addordel.html")

    app.run()


if __name__ == '__main__':
    main()
