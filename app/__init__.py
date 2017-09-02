# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Jinja extensions
app.jinja_env.add_extension('jinja2.ext.do')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_home.controllers import mod_home as home_module
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_users.controllers import mod_users as users_module
from app.mod_tasks.controllers import mod_tasks as tasks_module

# Register blueprint(s)
app.register_blueprint(home_module)
app.register_blueprint(auth_module)
app.register_blueprint(users_module)
app.register_blueprint(tasks_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
