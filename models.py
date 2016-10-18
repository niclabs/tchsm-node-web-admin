from werkzeug.security import generate_password_hash, check_password_hash
from nodeadmin import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(100), unique=True, index=True)
    password = db.Column('password', db.String(100))
    keys = db.relationship('Key', backref='user', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.email


class Key(db.Model):
    __tablename__ = 'keys'
    id = db.Column('key_id', db.Integer, primary_key=True)
    name = db.Column('key_name', db.String(100), index=True)
    data = db.Column('key', db.String(2000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, data, user):
        self.name = name
        self.data = data
        self.user = user

    def __repr__(self):
        return '<Key %r>' % self.name
