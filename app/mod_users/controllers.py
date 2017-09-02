from flask import Blueprint, request, render_template, abort, \
                  flash, g, session, redirect, url_for
from app import db
from app.mod_users.models import User

mod_users = Blueprint('users', __name__, url_prefix='/users')

@mod_users.route('/')
def index():
  users = User.query.all()
  return render_template('users/index.html', users=users)

@mod_users.route('/<username>')
def show(username):
  abort(401)

# @mod_users.route('/new', methods=['GET'])
# def new():
#   if not session.get('logged_in'):
#     abort(401)
#   form = TaskForm(request.form)
#   return render_template('tasks/new.html', form=form)
#
# @mod_users.route('/create', methods=['POST'])
# def create():
#   if not session.get('logged_in'):
#     abort(401)
#   form = TaskForm(request.form)
#
#   if form.validate():
#     task = Task(form.title.data, form.description.data, User.query.get(session.get('user_id')))
#     db.session.add(task)
#     db.session.commit()
#     flash('Task was successfully posted')
#     return redirect(url_for('tasks.index'))
#   else:
#     flash('Validations failed')
#   return render_template('tasks/new.html', form=form)
#
# @mod_users.route('/<id>', methods=['GET'])
# def show(id):
#   task = Task.query.get(id)
#   if not task:
#     flash('Task does not exist')
#     return redirect(url_for('tasks.index'))
#   return render_template('tasks/show.html', task=task)
#
# @mod_users.route('/<id>/complete', methods=['POST'])
# def complete(id):
#   if not session.get('logged_in'):
#     abort(401)
#   task = Task.query.get(id)
#   if not task:
#     flash('Task does not exist')
#     return redirect(url_for('index'))
#   if task.completed_by:
#     flash('Task is already completed')
#     return redirect(url_for('tasks.show', id=task.id))
#   task.complete(User.query.get(session.get('user_id')))
#   db.session.add(task)
#   db.session.commit()
#   flash('Task successfully completed')
#   return redirect(url_for('tasks.show', id=task.id))
#
# @mod_users.route('/<id>/delete', methods=['POST'])
# def delete(id):
#   if not session.get('logged_in'):
#     abort(401)
#   task = Task.query.get(id)
#   if not task:
#     flash('Task does not exist')
#     return redirect(url_for('index'))
#   if task.completed_by:
#     flash('Task is already completed. Unable to delete')
#     return redirect(url_for('tasks.show', id=task.id))
#   db.session.delete(task)
#   db.session.commit()
#   flash('Task successfully deleted')
#   return redirect(url_for('tasks.index'))
