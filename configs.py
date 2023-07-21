#Import buildint libriairies
import os
from typing import Tuple

#Import External librairies
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Projest's modules
from constants import DATABASE_NAME


def configs() -> Tuple[SQLAlchemy, Marshmallow]:
    '''
        This setting up the necessary tools who will be use on the wold project 
    '''
    
    rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "controllers"))
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Create the connexion application instance
    connex_app = connexion.App(__name__, specification_dir=rootdir)

    # Get the underlying Flask app instance
    app = connex_app.app

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
    
    return connex_app, db, ma
    
connexion_app, database, marsmallow = configs()