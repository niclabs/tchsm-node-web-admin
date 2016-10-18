from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.config.from_object('config.DefaultConfig')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


from models import User, Key
from forms import *


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is None:
            flash('Username doesn\'t exist', 'error')
            return redirect(url_for('login'))
        if not user.check_password(password):
            flash('Invalid password', 'error')
            return redirect(url_for('login'))
        login_user(user)
        flash('Successfully logged in', 'error')
        return redirect('/keys')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        user = User(email, password)
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/keys', methods=['GET', 'POST'])
@login_required
def keys():
    form = KeyCreationForm(request.form)
    key_list = Key.query.filter_by(user_id=int(current_user.get_id())).all()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        key = form.key.data
        user = current_user
        new_key = Key(name, key, user)
        db.session.add(new_key)
        db.session.commit()
        return redirect(url_for('keys'))
    return render_template('keys.html', form=form, key_list=key_list)


@app.route('/delete_key/<int:key_id>')
@login_required
def delete_key(key_id):
    key = Key.query.get(key_id)
    db.session.delete(key)
    db.session.commit()
    return redirect(url_for('keys'))


@app.route("/logout")
@login_required
def logout():
    flash('User %s logged out' % current_user.email)
    logout_user()
    return redirect(url_for('login'))




if __name__ == "__main__":
    app.run()
