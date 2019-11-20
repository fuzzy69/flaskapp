# -*- coding: UTF-8 -*-

from os.path import isfile
import logging

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from application.misc import StaticFilesFilter
from application.models import init_db
from config import DB_FILE, DB_URI, DEBUG, ROOT_DIR, SECRET_KEY, STATIC_DIR, TEMPLATES_DIR, __title__, version


# Filter static files info from Flask log
flask_log = logging.getLogger("werkzeug")
flask_log.addFilter(StaticFilesFilter())

# App
app = Flask(
    __name__,
    static_folder=STATIC_DIR,
    template_folder=TEMPLATES_DIR,
)
app.secret_key = SECRET_KEY
app.config["SCRIPT_ROOT"] = ROOT_DIR
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DATABASE_CONNECT_OPTIONS"] = {}

# DB
db = SQLAlchemy(app)
if not isfile(DB_FILE):
    init_db(DB_URI)

# Auth
login_manager = LoginManager()
login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(user_id):
#     """"""
#     return User.get(user_id)
    # return 12345


@app.context_processor
def ctx():
    """Variables/constants accessible from all templates"""
    return {
        "site_title": __title__,
        "version": version,
        "debug": DEBUG,
    }


@app.teardown_request
def teardown_request(exception):
    """Rollback transaction on error"""
    if exception:
        db.session.rollback()
        db.session.remove()
    db.session.remove()


# Error handlers
@app.errorhandler(404)
def _page_not_found(err):
    """Custom 404 error handler"""
    if request.path.startswith("/api/"):
        message = "API endpoint {!r} does not exist on this server!".format(request.path)
        return jsonify({
            "error": True,
            "message": message
        }), err.code

    message = "Page {!r} does not exist on this server!".format(request.path)
    flash(message, "warning")

    return redirect(url_for("front._page_not_found"))


@app.errorhandler(401)
def _unauthorized(err):
    """Custom 401 error handler"""
    message = "The server could not verify that you are authorized to access the URL requested!"
    if request.path.startswith("/api/"):
        return jsonify({
            "error": True,
            "message": message
        }), err.code
    flash(message, "warning")

    return render_template(
        "error.html",
        title="Unauthorized"
    ), err.code


from application.api import api
from application.backend import back
from application.frontend import front
from application.xhr import xhr


# Blueprints
app.register_blueprint(back)
app.register_blueprint(front)
app.register_blueprint(xhr)
app.register_blueprint(api)
