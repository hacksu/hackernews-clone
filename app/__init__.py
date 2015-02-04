from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# Create flask app
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# import our own modules
from users import controller
from links import controller