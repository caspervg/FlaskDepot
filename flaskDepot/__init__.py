from flask import Flask, send_from_directory
from flask.ext.login import login_required
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache
from flaskDepot.config import *


# Caches
usergroup_cache = SimpleCache()

# Application
app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.line_statement_prefix = '%'
app.jinja_env.line_comment_prefix = '##'

# Database
db = SQLAlchemy(app, session_options=dict(expire_on_commit=False))

import views.user
import views.file
import views.index
import views.search
import views.base
import views.errors