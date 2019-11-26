from flask import Flask
from config import configure
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

'''
Initialization manager
'''
app = Flask(__name__)
app.config.from_object(configure)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)

from flask_ex import routes, models
