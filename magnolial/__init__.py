from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
db.Base = declarative_base()

from magnolial.models import Magnolial, MagnolialUser
from magnolial.api import *
