from flask import Flask, redirect, url_for, render_template, request
from forms import *
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        print ("mail: %s, password: %s" % (form.email.data, form.password.data))
        return redirect('/keys')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        print ("mail: %s, password: %s password: %s" % (form.email.data, form.password.data, form.confirm.data))
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/keys')
def keys():
    return render_template('keys.html')


if __name__ == "__main__":
    app.run()
