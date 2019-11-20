# -*- coding: UTF-8 -*-

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from application.auth import User
from application.base import db
from application.forms import LoginForm
from application.models import UsersTable


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
        r = db.session.query(UsersTable).filter(UsersTable.username == username).first()
        if r is None or not check_password_hash(r.password, password):
            flash("Please enter valid username/password!", "danger")
            return redirect(url_for("front._login"))
        # OK
        user = User()
        user.id = username
        login_user(user)
        return redirect(url_for("back._index"))

    return render_template(
        "frontend/login.html",
        title="Login",
        form=form
    )


@front.route("/logout")
def _logout():
    """Logs out user and redirects to login page"""
    logout_user()
    flash("You've been logged out successfully", "info")

    return render_template(
        "frontend/logout.html",
        title="Logout"
    )


@front.route("/contact")
def _contact():
    """"""
    return render_template(
        "frontend/contact.html",
        title="Contact"
    )


@front.route("/404")
def _page_not_found():
    """"""

    return render_template(
        "error.html",
        title="Page Not Found"
    ), 404
