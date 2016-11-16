from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager
from os import environ
from libconf import load

def get_public_key(path):
	with open(path) as f:
		config = load(f)
		key = config.node.public_key
		return key

app = Flask(__name__)
app.config.from_object('config.DefaultConfig')

node_db_path = environ.get('NODE_DB_PATH')
if node_db_path is None:
	node_db_path = "node.db"
node_db_full_path = "sqlite:///" + node_db_path
app.config['SQLALCHEMY_DATABASE_URI'] = node_db_full_path

db = SQLAlchemy(app)

node_conf_path = environ.get('NODE_CONF_PATH')
if node_conf_path is None:
	node_conf_path = "node.conf"

public_key = get_public_key(node_conf_path)
app.config['NODE_PUBLIC_KEY'] = public_key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from nodeadmin.views import *
