from flask import Blueprint, request, render_template, flash, \
                  g, session, redirect, url_for, abort

mod_home = Blueprint('home', __name__)

@mod_home.route('/', methods=['GET'])
def index():
  return render_template("home/index.html")
