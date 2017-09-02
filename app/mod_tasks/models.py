# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from sqlalchemy import event
from datetime import datetime

# Define a base model for other database tables to inherit
class Base(db.Model):
  __abstract__  = True

  id            = db.Column(db.Integer, primary_key=True)
  date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
  onupdate=db.func.current_timestamp())

class Task(db.Model):
  __tablename__ = 'task'

  id              = db.Column(db.Integer, primary_key=True)
  title           = db.Column(db.String(80))
  description     = db.Column(db.Text)
  added_by_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
  created_at      = db.Column(db.DateTime)
  completed_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  completed_at    = db.Column(db.DateTime)

  added_by        = db.relationship('User', foreign_keys=[added_by_id], backref=db.backref('added_tasks'))
  completed_by    = db.relationship('User', foreign_keys=[completed_by_id], backref=db.backref('completed_tasks'))

  def __init__(self, title, description, added_by):
    self.title = title
    self.description = description
    self.added_by = added_by

  def __repr__(self):
    return 'Task %r, Added By %r, Completed By %r' % (self.title, self.added_by, self.completed_by)

  def complete(self, user):
    self.completed_by = user
    self.completed_at = datetime.now()

@event.listens_for(Task, 'before_insert')
def create_time(mapper, connection, target):
    target.created_at = datetime.now()
