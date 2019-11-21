# -*- coding: UTF-8 -*-

from flask import Blueprint, current_app, redirect, render_template, request, flash, url_for
from flask_login import login_required
from flask_paginate import Pagination

from application.base import db
from application.data import DataError, DataTable
from application.models import SettingsTable
from config import IPP, H5_FILE, OXTS_TABLE_COLUMNS


app = current_app
back = Blueprint("back", __name__, url_prefix="/back", template_folder="templates/backend")


def get_ipp() -> int:
    """Returns number of pagination items per page"""
    try:
        r = db.session.query(SettingsTable).first()
        ipp = r.items_per_page
    except:
        ipp = IPP
        message = "Failed to query settings data from database!"
        app.logger.warning(message, exc_info=True)
        flash(message, "danger")

    return ipp


@back.route('/')
@back.route("/index")
@login_required
def _index():
    """Backend home page"""
    return render_template(
        "index.html",
        title="Dummy Dashboard page"
    )

@back.route("/oxts", defaults={"page": 1})
@back.route("/oxts/<int:page>")
@login_required
def _oxts(page: int):
    """Shows OXTS data points"""
    rows = []
    pagination = None
    ipp = get_ipp()
    start = (page - 1) * ipp
    stop = start + ipp
    try:
        dt = DataTable(H5_FILE)
        filters = {}
        rows = [row for row in dt.fetch_rows_as_tuples(start, stop, **filters)]
        pagination = Pagination(page=page, total=dt.rows_count, per_page=ipp, bs_version=4)
    except (DataError, Exception):
        message = "Failed to query OXTS data!"
        app.logger.warning(message, exc_info=True)
        flash(message, "danger")

    return render_template(
        "oxts.html",
        title="OXTS",
        headers=OXTS_TABLE_COLUMNS,
        rows=rows,
        pagination=pagination,
        start=start,
    )


@back.route("/velo", defaults={"page": 1})
@back.route("/velo/<int:page>")
@login_required
def _velo(page: int):
    """Shows Velodyne data points"""
    rows = []
    pagination = None
    ipp = get_ipp()
    start = (page - 1) * ipp
    stop = start + ipp
    # TODO: Replace dummy OXTS data with real Velodyne data
    try:
        dt = DataTable(H5_FILE)
        filters = {}
        rows = [row for row in dt.fetch_rows_as_tuples(start, stop, **filters)]
        pagination = Pagination(page=page, total=dt.rows_count, per_page=ipp, bs_version=4)
    except (DataError, Exception):
        message = "Failed to query Velodyne data!"
        app.logger.warning(message, exc_info=True)
        flash(message, "danger")

    return render_template(
        "oxts.html",
        title="Velodyne",
        headers=OXTS_TABLE_COLUMNS,
        rows=rows,
        pagination=pagination,
        start=start,
    )


@back.route("/settings", methods=["GET", "POST"])
@login_required
def _settings():
    """Shows and updates app settings"""
    # FIXME: Improve code flow
    if request.method == "POST":
        ipp = request.form.get("ipp")
        if ipp is None:
            flash("Invalid items per page value! Please select value from 10 to 100.", "danger")
        else:
            try:
                ipp = int(ipp)
                if ipp < 10 or ipp > 100:
                    ipp = None
                    flash("Invalid items per page value! Please select value from 10 to 100.", "danger")
            except ValueError:
                ipp = None
                message = "Invalid items per page value! Please select value from 10 to 100."
                app.logger.warning(message, exc_info=True)
                flash(message, "danger")
            if ipp is not None:
                try:
                    r = db.session.query(SettingsTable).first()
                    r.items_per_page = ipp
                    db.session.commit()
                    flash("Successfully updated settings!", "success")
                except:
                    message = "Failed to query settings data from database!"
                    flash(message, "danger")
                    app.logger.warning(message, exc_info=True)
        return redirect(url_for("back._settings"))

    ipp = get_ipp()

    return render_template(
        "settings.html",
        title="Settings",
        ipp=ipp
    )
