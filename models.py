from werkzeug.security import generate_password_hash, check_password_hash
from nodeadmin import db


class User(db.Model):
    __tablename__ = 'user'
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


class Instance(db.Model):
    # this schema must replicate the one defined by the node database in tchsm-libdtc
    __tablename__ = 'instance'
    instance_id = db.Column('instance_id', db.Text, primary_key=True)
    public_key = db.Column('public_key', db.Text, unique=True)
    router_token = db.Column('router_token', db.Text)
    pub_token = db.Column('pub_token', db.Text)

    def __init__(self, instance_id, public_key):
        self.instance_id = instance_id
        self.public_key = public_key
        self.router_token = ""
        self.pub_token = ""

    def __repr__(self):
        return '<Instance %r, key %r>' % (self.instance_id, self.public_key)


class Key(db.Model):
    __tablename__ = 'user_key'
    id = db.Column('key_id', db.Integer, primary_key=True)
    tag = db.Column('key_name', db.String(100), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    instance_id = db.Column(db.Text, db.ForeignKey('instance.instance_id'))
    instance = db.relationship(Instance)

    def __init__(self, tag, user, instance):
        self.tag = tag
        self.user = user
        self.instance = instance

    def __repr__(self):
        return '<Key %r from %r>' % (self.tag, self.user)
