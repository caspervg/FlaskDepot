"""
Flask-Depot
=======

Flask-Depot is a filesharing application written in the Python web-framework Flask
"""
from setuptools import setup

setup(
    name='FlaskDepot',
    version='0.0.1-indev',
    url='https://github.com/caspervg/FlaskDepot',
    license='MIT',
    author='CasperVg',
    author_email='caspervg@gmail.com',
    description='A filesharing application written with the web-framework Flask',
    long_description=__doc__,
    packages=['flaskdepot'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask==0.10.1',
        'Flask-Login==0.2.10',
        'Flask-Mail==0.9.0',
        'Flask-Migrate==1.2.0',
        'Flask-SQLAlchemy==1.0',
        'Flask-Script==0.6.7',
        'Flask-WTF==0.9.4',
        'Jinja2==2.7.2',
        'SQLAlchemy==0.9.3',
        'WTForms==1.0.5',
        'Werkzeug==0.9.4',
        'alembic==0.6.3',
        'slugify',
        'Flask-WhooshAlchemy',
        'Flask-Bcrypt'
    ],
    dependency_links=[
        'https://github.com/miguelgrinberg/Flask-WhooshAlchemy/tarball/master#egg=Flask-WhooshAlchemy',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers, Users',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
