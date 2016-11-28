from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager
from os import environ
from libconf import load

def MissingEnvironmentVariableException(Exception):
	pass

def get_public_key(path):
	with open(path) as f:
		config = load(f)
		key = config.node.public_key
		return key

def get_db_path(path):
	with open(path) as f:
		config = load(f)
		db_path = config.node.database
		return db_path

app = Flask(__name__)
app.config.from_object('config.DefaultConfig')

node_conf_path = environ.get('NODE_CONF_PATH')
if node_conf_path is not None:
	public_key = get_public_key(node_conf_path)
	app.config['NODE_PUBLIC_KEY'] = public_key
	db_path = get_db_path(node_conf_path)
	node_db_full_path = "sqlite:///" + db_path
	app.config['SQLALCHEMY_DATABASE_URI'] = node_db_full_path

else:
	print("Warning: environment variable NODE_CONF_PATH wasn't set. Default value %s will be used for the node public key" 
		% app.config['NODE_PUBLIC_KEY'])

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from nodeadmin.views import *
