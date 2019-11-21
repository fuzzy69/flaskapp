# -*- coding: UTF-8 -*-

from flask import Blueprint, current_app, render_template, flash
from flask_login import login_required
from flask_paginate import Pagination

from application.data import DataError, DataTable
from config import IPP, H5_FILE, OXTS_TABLE_COLUMNS


app = current_app
back = Blueprint("back", __name__, url_prefix="/back", template_folder="templates/backend")


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
    start = (page - 1) * IPP
    stop = start + IPP
    try:
        dt = DataTable(H5_FILE)
        filters = {}
        rows = [row for row in dt.fetch_rows_as_tuples(start, stop, **filters)]
        pagination = Pagination(page=page, total=dt.rows_count, per_page=IPP, bs_version=4)
    except (DataError, Exception):
        message = "Failed to query OXTS data!"
        flash(message, "danger")
        app.logger.warning(message, exc_info=True)

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
    start = (page - 1) * IPP
    stop = start + IPP
    # TODO: Replace dummy OXTS data with real Velodyne data
    try:
        dt = DataTable(H5_FILE)
        filters = {}
        rows = [row for row in dt.fetch_rows_as_tuples(start, stop, **filters)]
        pagination = Pagination(page=page, total=dt.rows_count, per_page=IPP, bs_version=4)
    except (DataError, Exception):
        message = "Failed to query Velodyne data!"
        flash(message, "danger")
        app.logger.warning(message, exc_info=True)

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
    return render_template(
        "index.html"
    )
