from flask import Flask, render_template
from flaskdepot.extensions import db, login_manager, mail, migrate


def configure_blueprints(app):
    """
    Configures the blueprints
    """

    from flaskdepot.user.views import user
    from flaskdepot.base.views import base
    # from flaskdepot.auth.views import auth
    #from flaskdepot.admin.views import admin
    from flaskdepot.file.views import file
    from flaskdepot.search.views import search

    app.register_blueprint(file, url_prefix=app.config["FILE_PREFIX"])
    app.register_blueprint(user, url_prefix=app.config["USER_PREFIX"])
    app.register_blueprint(search, url_prefix=app.config["SEARCH_PREFIX"])
    app.register_blueprint(base)
    #app.register_blueprint(auth, url_prefix=app.config["AUTH_PREFIX"])
    #app.register_blueprint(admin, url_prefix=app.config["ADMIN_PREFIX"])


def configure_extensions(app):
    """
    Configures the Flask extensions
    """
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """
        Loads the current user for Flask-Login
        """
        from flaskdepot.user.models import User
        return db.session.query(User).get(user_id)

    login_manager.init_app(app)


def configure_filters(app):
    pass


def configure_handlers(app):
    @app.errorhandler(401)
    def unauthorized(e):
        return render_template("error.html", name=u'Unauthorized',
                               message=u'Sorry, but you need to log in to access this page'), 401


    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error.html", name=u'Forbidden',
                               message=u'Sorry, but you do not have access to this page'), 403


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error.html", name=u'Not Found',
                               message=u'Sorry, the page you were looking for could not be found'), 404


    @app.errorhandler(410)
    def gone(e):
        return render_template("error.html", name=u'Gone',
                               message=u'Sorry, the page you were looking for is not accessible'), 410


    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("error.html", name=u'Server Error',
                               message=u'Sorry, the server encountered an error while processing your request.'
                                       u' Please try again later.'
                                       u' If this problem persists, contact the administration'), 500


def configure_requests(app):
    pass


def create_app(config=None):
    """
    Creates the application
    """
    app = Flask("flaskdepot")

    # Default configuration
    app.config.from_object('flaskdepot.configs.default.DefaultConfig')
    # Update the configuration if it exists in the parameters
    app.config.from_object(config)
    # Update the configuration based on environment variables
    app.config.from_envvar("FLASKDEPOT_CONFIG", silent=True)

    configure_blueprints(app)
    configure_extensions(app)
    configure_filters(app)
    configure_handlers(app)
    configure_requests(app)

    return app