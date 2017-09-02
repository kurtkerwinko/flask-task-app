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
  user = User.query.filter_by(username=username).first()
  if not user:
    flash('User does not exist')
    return redirect(url_for('users.index'))
  return render_template('users/show.html', user=user)
