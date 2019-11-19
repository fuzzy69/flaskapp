# -*- coding: UTF-8 -*-

from os.path import isfile
from itertools import islice

from flask import Blueprint, render_template, flash
from flask_paginate import Pagination, get_page_parameter
from pandas import DataFrame, read_csv
import tables

# from application.base import app
from config import IPP, H5_FILE, OXTS_CSV_FILE, OXTS_TABLE_COLUMNS


back = Blueprint("back", __name__, url_prefix="/back", template_folder="templates/backend")


@back.route('/')
@back.route("/index")
def _index():
    """Index page"""
    return render_template(
        "index.html"
    )

@back.route("/oxts", defaults={"page": 1})
@back.route("/oxts/<int:page>")
def _oxts(page: int):
    """Shows OXTS data points"""
    rows = []
    pagination = None
    start = (page - 1) * IPP
    stop = start + IPP
    if isfile(H5_FILE):
        h5file = None
        try:
            h5file = tables.open_file(H5_FILE, mode="r")
            table = h5file.root.sequences.oxts
            total_rows = table.shape[0]
            rows = [tuple(row[attr].decode("utf-8") if attr == "timestamp" else row[attr]
                        for attr in OXTS_TABLE_COLUMNS)
                            for row in table.iterrows(start, stop)]
            pagination = Pagination(page=page, total=total_rows, per_page=IPP, bs_version=4)
        except:
            msg = "Failed to query KITTI data file!"
            flash(msg, "danger")
            # app.logger.warning(msg, exc_info=True)
        finally:
            if h5file is not None:
                h5file.close()
    else:
        msg = "Failed to locate KITTI data file!"
        flash(msg, "danger")
        # app.logger.warning(msg, exc_info=True)

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
def _velo(page: int):
    """Shows Velodyne data points"""
    rows = []
    pagination = None
    start = (page - 1) * IPP
    stop = start + IPP
    if isfile(H5_FILE):
        h5file = None
        try:
            h5file = tables.open_file(H5_FILE, mode="r")
            table = h5file.root.sequences.oxts
            total_rows = table.shape[0]
            rows = [tuple(row[attr] for attr in OXTS_TABLE_COLUMNS) for row in table.iterrows(start, stop)]
            pagination = Pagination(page=page, total=total_rows, per_page=IPP, bs_version=4)
        except:
            pass
        finally:
            if h5file is not None:
                h5file.close()
    else:
        msg = "Failed to locate KITTI data file!"
        flash(msg, "danger")
        # app.logger.warning(msg, exc_info=True)

    return render_template(
        "oxts.html",
        title="Velodyne",
        headers=OXTS_TABLE_COLUMNS,
        rows=rows,
        pagination=pagination,
        start=start,
    )


@back.route("/settings", methods=["GET", "POST"])
def _settings():
    """Shows and updates app settings"""
    return render_template(
        "index.html"
    )
