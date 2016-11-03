class DefaultConfig(object):
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = 'app secret key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/caterina/node_1.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NODE_PUBLIC_KEY = 'node public key'