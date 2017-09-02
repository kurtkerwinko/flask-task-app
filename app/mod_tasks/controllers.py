# Import flask dependencies
from flask import Blueprint, request, render_template, abort, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import app, db

# Import module forms
from app.mod_tasks.forms import TaskForm

# Import module models (i.e. User)
from app.mod_tasks.models import Task
from app.mod_users.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_tasks = Blueprint('tasks', __name__, url_prefix='/tasks')

# Set the route and accepted methods
@mod_tasks.route('/')
def index():
  fltr = request.args.get('s')
  page = 1 if request.args.get('page')==None else int(request.args.get('page'))
  tasks = Task.query
  if fltr == 'c':
    tasks = Task.query.filter(Task.completed_by != None)
  elif fltr == 'nc':
    tasks = Task.query.filter_by(completed_by=None)
  tasks = tasks.paginate(page, app.config["ITEMS_PER_PAGE"], False)
  return render_template('tasks/index.html', tasks=tasks)

@mod_tasks.route('/new', methods=['GET'])
def new():
  if not session.get('logged_in'):
    abort(401)
  form = TaskForm(request.form)
  return render_template('tasks/new.html', form=form)

@mod_tasks.route('/create', methods=['POST'])
def create():
  if not session.get('logged_in'):
    abort(401)
  form = TaskForm(request.form)

  if form.validate():
    task = Task(form.title.data, form.description.data, User.query.get(session.get('user_id')))
    db.session.add(task)
    db.session.commit()
    flash('Task was successfully posted')
    return redirect(url_for('tasks.index'))
  else:
    flash('Validations failed')
  return render_template('tasks/new.html', form=form)

@mod_tasks.route('/<id>', methods=['GET'])
def show(id):
  task = Task.query.get(id)
  if not task:
    flash('Task does not exist')
    return redirect(url_for('tasks.index'))
  return render_template('tasks/show.html', task=task)

@mod_tasks.route('/<id>/complete', methods=['POST'])
def complete(id):
  if not session.get('logged_in'):
    abort(401)
  task = Task.query.get(id)
  if not task:
    flash('Task does not exist')
    return redirect(url_for('index'))
  if task.completed_by:
    flash('Task is already completed')
    return redirect(url_for('tasks.show', id=task.id))
  task.complete(User.query.get(session.get('user_id')))
  db.session.add(task)
  db.session.commit()
  flash('Task successfully completed')
  return redirect(url_for('tasks.show', id=task.id))

@mod_tasks.route('/<id>/delete', methods=['POST'])
def delete(id):
  if not session.get('logged_in'):
    abort(401)
  task = Task.query.get(id)
  if not task:
    flash('Task does not exist')
    return redirect(url_for('index'))
  if task.completed_by:
    flash('Task is already completed. Unable to delete')
    return redirect(url_for('tasks.show', id=task.id))
  db.session.delete(task)
  db.session.commit()
  flash('Task successfully deleted')
  return redirect(url_for('tasks.index'))
