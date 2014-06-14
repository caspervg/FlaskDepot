"""
    flaskdepot.extensions
    ~~~~~~~~~~~~~~~~~~~~

    The extensions that are used by FlaskDepot

    :copyright: (c) 2014 by CasperVg.
    :license: MIT, see LICENSE for more details.
"""

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.migrate import Migrate

# Database
db = SQLAlchemy()

# Login
login_manager = LoginManager()

# Mail
mail = Mail()

# Migrations
migrate = Migrate()
