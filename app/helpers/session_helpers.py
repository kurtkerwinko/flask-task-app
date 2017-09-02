from flask import session, redirect, url_for

def redirect_logged_in():
  if session.get('logged_in'):
    return redirect(url_for('home.index'))

# from app.helpers.session_helpers import already_logged_in
