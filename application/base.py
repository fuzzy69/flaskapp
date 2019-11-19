# -*- coding: UTF-8 -*-

import logging

from flask import Flask, jsonify, render_template, request
from flask_login import LoginManager

# from application.api import api
# from application.backend import back
# from application.frontend import front
from application.misc import StaticFilesFilter
# from application.xhr import xhr
from config import DEBUG, ROOT_DIR, SECRET_KEY, STATIC_DIR, TEMPLATES_DIR, __title__, version


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

# # Blueprints
# app.register_blueprint(back)
# app.register_blueprint(front)
# app.register_blueprint(xhr)
# app.register_blueprint(api)

# Auth
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """"""
    # return User.get(user_id)
    return 12345


@app.context_processor
def ctx():
    """Variables/constants accessible from all templates"""
    return {
        "site_title": __title__,
        "version": version,
        "debug": DEBUG,
    }


@app.errorhandler(404)
def _page_not_found(err):
    """"""
    if request.path.startswith("/api/"):
        return jsonify(
            {'error': True, 'msg': 'API endpoint {!r} does not exist on this server'.format(request.path)}), err.code

    return render_template(
        "404.html",
        title="Page Not Found"
    ), 404


from application.api import api
from application.backend import back
from application.frontend import front
from application.xhr import xhr


# Blueprints
app.register_blueprint(back)
app.register_blueprint(front)
app.register_blueprint(xhr)
app.register_blueprint(api)
