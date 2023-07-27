import os

DATABASE_NAME = "database.sqlite"
STATIC_PATH = os.path.join('frontend', 'static')
TEMPLATES_PATH = os.path.join('frontend', 'templates')
UPLOADED_FILES = os.path.abspath(os.path.join(os.path.dirname(__file__), STATIC_PATH, 'uploaded'))