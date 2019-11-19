# -*- coding: UTF-8 -*-

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from application.auth import USERS
from application.forms import LoginForm

app = current_app
front = Blueprint("front", __name__)


@front.route('/')
def _index():
    """Home page"""
    return render_template(
        "frontend/index.html",
        title="Home"
    )


@front.route("/login", methods=["GET", "POST"])
def _login():
    """User login page"""
    form = LoginForm()
    # if form.validate_on_submit():
    #     return redirect("/contact")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not all((username, password)):
            flash("Please enter username and password!", "danger")
            return redirect(url_for("front._login"))
        if username not in USERS or not check_password_hash(USERS[username], password):
            flash("Please enter valid username/password!", "danger")
            return redirect(url_for("front._login"))
        # OK
        return redirect(url_for("back._index"))

    return render_template(
        "frontend/login.html",
        title="Login",
        form=form
    )


@front.route("/logout")
def _logout():
    """Logs out user and redirects to login page"""
    if request.method == "POST":
        pass

    return render_template(
        "frontend/login.html",
        title="Login"
    )


@front.route("/contact")
def _contact():
    """"""
    return render_template(
        "frontend/contact.html",
        title="Contact"
    )
