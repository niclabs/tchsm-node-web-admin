class DefaultConfig(object):
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = 'your-secret-key-goes-here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False