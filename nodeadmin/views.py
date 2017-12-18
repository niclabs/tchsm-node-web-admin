from flask import redirect, url_for, render_template, request, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from nodeadmin import app, login_manager, db
from nodeadmin.models import *
from nodeadmin.forms import *

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
        next = request.args.get('next')
        flash('Successfully logged in', 'error')
        return redirect(next or url_for('keys'))
    return render_template('login.html', form=form)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = PasswordChangeForm(request.form)
    if request.method == 'POST' and form.validate():
        current_password = form.current_password.data
        new_password = form.new_password.data
        user = current_user
        if not current_user.check_password(current_password):
            flash('Invalid password', 'error')
            return redirect(url_for('change_password'))
        current_user.set_password(new_password)
        db.session.add(user)
        db.session.commit()
        flash('User successfully updated')
        return redirect(url_for('keys'))
    return render_template('change_password.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        user = User(email, password)
        db.session.add(user)
        db.session.commit()
        flash('User %s successfully registered' % email)
        return redirect(url_for('keys'))
    return render_template('register.html', form=form)


@app.route('/keys', methods=['GET', 'POST'])
@login_required
def keys():
    form = KeyCreationForm(request.form)
    key_list = Key.query.filter_by(user_id=int(current_user.get_id())).all()
    if request.method == 'POST' and form.validate():
        instance_id = form.instance_id.data
        key = form.key.data
        user = current_user
        new_instance = Instance(instance_id, key)
        new_key = Key(user, new_instance)
        try:
            db.session.add(new_instance)
            db.session.add(new_key)
            db.session.commit()
        except IntegrityError as e:
            flash("The database already has a key with that instance id.")
            return redirect(url_for('keys'))
        return redirect(url_for('keys'))
    return render_template('keys.html', form=form, key_list=key_list)

@app.route('/edit_key/<int:key_id>', methods=['GET', 'POST'])
@login_required
def edit_key(key_id):
    if not user_owns_key(key_id):
        abort(403)
    key = Key.query.get_or_404(key_id)
    instance = key.instance
    form = KeyEditionForm(request.form)
    if request.method == 'POST' and form.validate():
        instance.public_key = form.key.data
        db.session.add(key)
        db.session.add(instance)
        db.session.commit()
        return redirect(url_for('keys'))
    form.key.data = instance.public_key
    return render_template('edit_key.html', key_id=key.id, form=form)


@app.route('/delete_key/<int:key_id>')
@login_required
def delete_key(key_id):
    if not user_owns_key(key_id):
        abort(403)
    key = Key.query.get_or_404(key_id)
    instance = key.instance
    db.session.delete(instance)
    db.session.delete(key)
    db.session.commit()
    return redirect(url_for('keys'))


@app.route("/logout")
@login_required
def logout():
    flash('User %s logged out' % current_user.email)
    logout_user()
    return redirect(url_for('login'))


def user_owns_key(key_id):
    user = current_user
    key = Key.query.get_or_404(key_id)
    return key.user_id == user.id

