# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
  __abstract__  = True

  id            = db.Column(db.Integer, primary_key=True)
  date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
  onupdate=db.func.current_timestamp())

class User(db.Model):
  id         = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(30))
  last_name  = db.Column(db.String(30))
  username   = db.Column(db.String(80), unique=True)
  password   = db.Column(db.String(120))

  def __init__(self, first_name, last_name, username, password):
    self.first_name = first_name
    self.last_name = last_name
    self.username = username
    self.password = password

  def __repr__(self):
    return '%s %s' % (self.first_name, self.last_name)
