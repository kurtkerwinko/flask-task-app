# Import flask dependencies
from flask import Blueprint, request, render_template, abort, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_users.forms import LoginForm, SignUpForm

# Import module models (i.e. User)
from app.mod_users.models import User

# Helper functions
from app.helpers.session_helpers import redirect_logged_in

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.before_request
def logged_in():
  if request.endpoint != 'auth.logout':
    return redirect_logged_in()

@mod_auth.route('/signup/', methods=['GET'])
def signup():
  form = SignUpForm(request.form)
  return render_template("auth/signup.html", form=form)

@mod_auth.route('/create/', methods=['POST'])
def create():
  form = SignUpForm(request.form)
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if not user:
      user = User(form.first_name.data, form.last_name.data, form.username.data, generate_password_hash(form.password.data))
      db.session.add(user)
      db.session.commit()
      flash('Created account. Please signin')
      return redirect(url_for('auth.signin'))
    flash('Username exists', 'error-message')
  return render_template("auth/signup.html", form=form)


# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
  # If sign in form is submitted
  form = LoginForm(request.form)

  # Verify the sign in form
  if request.method == 'POST':
    if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).first()
      if user and check_password_hash(user.password, form.password.data):
        session['logged_in'] = True
        session['user_id'] = user.id
        flash('Welcome %s' % user.first_name )
        return redirect(url_for('tasks.index'))
      flash('Wrong email or password', 'error-message')
  return render_template("auth/signin.html", form=form)

@mod_auth.route('/logout', methods=['POST'])
def logout():
  session.pop('logged_in', None)
  session.pop('user_id', None)
  flash('You were logged out')
  return redirect(url_for('tasks.index'))
