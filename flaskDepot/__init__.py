from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache
from config import *

# Caches
usergroup_cache = SimpleCache()

# Application
app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.line_statement_prefix = '%'
app.jinja_env.line_comment_prefix = '##'

# Database
db = SQLAlchemy(app, session_options=dict(expire_on_commit=False))

import views.base
import views.user
import views.file

