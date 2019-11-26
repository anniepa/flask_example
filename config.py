import os

base_directory = os.path.abspath(os.path.dirname(__file__))

'''
Quick and dirty configuration for SQL database
'''
class configure(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "wrong"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_directory, 'flask_sample.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
