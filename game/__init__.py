import flask_admin
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('..\config.py')
db = SQLAlchemy(app)

from game import controllers, models

