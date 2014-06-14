"""
    flaskdepot.manage
    ~~~~~~~~~~~~~~~~~~~~

    This script provides some commands for setting up your flaskdepot and managing it

    :copyright: (c) 2014 by CasperVg.
    :license: MIT, see LICENSE for more details.
"""
import sys

from flask import current_app
from sqlalchemy.exc import IntegrityError, OperationalError
from flask.ext.script import (Manager, Shell, Server, prompt, prompt_pass,
                              prompt_bool)
from flask.ext.migrate import MigrateCommand
from flaskdepot.app import create_app
from flaskdepot.extensions import db
from flaskdepot.utils.populate import create_default_groups, create_admin_user, create_normal_user, create_sample_data

# Use the development configuration if available
from flaskdepot.user.models import Usergroup

try:
    from flaskdepot.configs.development import DevelopmentConfig as Config
except ImportError:
    from flaskdepot.configs.default import DefaultConfig as Config

app = create_app(Config)
manager = Manager(app)

# Run local server
manager.add_command("runserver", Server("localhost", port=8080))

# Migration commands
manager.add_command('db', MigrateCommand)


# Add interactive project shell
def make_shell_context():
    return dict(app=current_app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def initdb():
    """Creates the database."""

    db.create_all()


@manager.command
def dropdb():
    """Deletes the database"""

    db.drop_all()


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_admin(username=None, password=None, email=None):
    """Creates the admin user"""

    if not (username and password and email):
        username = prompt("Username")
        email = prompt("A valid email address")
        password = prompt_pass("Password")

    create_admin_user(username=username, password=password, email=email)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_user(username=None, password=None, email=None):
    """Creates a normal user"""

    if not (username and password and email):
        username = prompt("Username")
        email = prompt("A valid email address")
        password = prompt_pass("Password")

    create_normal_user(username=username, password=password, email=email)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def initdepot(username=None, password=None, email=None):
    """Initializes FlaskBB with all necessary data"""

    app.logger.info("Creating default groups...")
    try:
        create_default_groups()
    except IntegrityError:
        app.logger.error("Couldn't create the default groups because they are already exist!")
        if prompt_bool("Do you want to recreate the database? (y/n)"):
            db.session.rollback()
            db.drop_all()
            db.create_all()
            create_default_groups()
        else:
            sys.exit(0)
    except OperationalError:
        app.logger.error("No database found.")
        if prompt_bool("Do you want to create the database? (y/n)"):
            db.session.rollback()
            db.create_all()
            create_default_groups()
        else:
            sys.exit(0)

    app.logger.info("Creating admin user...")
    if username and password and email:
        create_admin_user(username=username, password=password, email=email)
    else:
        create_admin()


    app.logger.info("Creating normal user...")
    create_user()

    app.logger.info("Creating sample data...")
    create_sample_data()

    app.logger.info("Congratulations! FlaskBB has been successfully installed")


if __name__ == "__main__":
    manager.run()
