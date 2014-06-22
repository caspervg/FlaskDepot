flask-depot
==========
Python (Flask) based file-exchange web application. Still in development.

### Live demo
A live demo of a FlaskDepot can be found at [flaskdepot.caspervg.net](http://flaskdepot.caspervg.net). It is not guaranteed to be 100% up to date with the source code at all times, but I try to update it regularly. 

### Current features
* Admin panel with full control over users, groups, categories and files
* File upload form with basic versioning support
* Basic user register/login form
* File categorisation on two levels (broad and narrow categories)
* File locking/deleting/editing for admins and authors
* Basic file evaluation with comments and ratings
* Uses Foundation v5 layout with as little changes as possible, so very easy to style to your demand
* File slugs
* Follows REST principles as much as possible

### Planned features
* More detailed user profiles (avatars, etc.) and optional OpenID integration
* Dependency tracking system
* More intricate rating and evaluation support (reviews, ..)
* Changelog support + optional support for keeping/downloading old versions of files
* Private files (select who can see and download files)
* Featured file system (displayed prominently on the index page)
* Optional integration with Google Analytics, etc.
* Easy database migration using Flask-Migrate and Alembic
* Password reset form
* E-mail activation of new users
* Full JSON/XML API support for (mobile) applications

### Dependencies
* Flask==0.10.1
* Flask-Login==0.2.10
* Flask-Mail==0.9.0
* Flask-SQLAlchemy==1.0
* Flask-WTF==0.9.4
* Jinja2==2.7.2
* SQLAlchemy==0.9.3
* WTForms==1.0.5
* Werkzeug==0.9.4
* slugify
