#Import buildint libriairies
import os
from typing import Tuple

#Import External librairies
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Projest's modules
from constants import DATABASE_NAME, STATIC_PATH, TEMPLATES_PATH


def configs() -> Tuple[Flask, SQLAlchemy, Marshmallow]:
    '''
        This setting up the necessary tools who will be use on the wold project 
    '''
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    app = Flask(__name__, static_folder=STATIC_PATH, template_folder=TEMPLATES_PATH)

    # Build the Sqlite ULR for SqlAlchemy
    DATABASE_PATH = os.path.join(basedir, DATABASE_NAME)
    sqlite_url = "sqlite:////" + DATABASE_PATH

    # Configure the SqlAlchemy part of the app instance
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Create the SqlAlchemy db instance
    db = SQLAlchemy(app)

    # Initialize Marshmallow
    ma = Marshmallow(app)
    
    return app, db, ma
    
connexion_app, database, marsmallow = configs()