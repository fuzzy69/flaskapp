# -*- coding: UTF-8 -*-

from datetime import datetime
from urllib.parse import unquote

from flask import Blueprint, current_app, request
from flask_login import login_required

from application.apiresult import APIResult
from application.data import DataTable
from application.errors import DataError
from config import version, IPP, H5_FILE


app = current_app
api = Blueprint("api", __name__, url_prefix="/api")


@api.route('/')
def _index():
    """API root endpoint, return API details"""
    r = APIResult(message="KITTI Flask Demo API")
    r.fields = ("status", "message", "version")

    return r.json()


@api.route("/oxts", defaults={"page": 1})
@api.route("/oxts/<int:page>")
@login_required
def _oxts(page: int):
    """Returns OXTS data points"""
    status = False
    message = ''
    data = None
    start = (page - 1) * IPP
    stop = start + IPP
    # Filters
    filters = {}
    timestamp = request.args.get("timestamp")
    if timestamp is not None:
        timestamp = unquote(timestamp)
        try:
            datetime.fromisoformat(timestamp)
            filters["timestamp"] = timestamp
        except ValueError:
            message = "Invalid timestamp argument format!"
            r = APIResult(status, message)
            r.fields = ("status", "message")
            app.logger.warning(message, exc_info=True)
            return r.json()
    try:
        dt = DataTable(H5_FILE)
        rows = [row for row in dt.fetch_rows_as_dicts(start, stop, **filters)]
        data = {
            "oxts": rows,
            "total_pages": dt.rows_count // IPP  # FIXME: should return number of selected pages
        }
        status = True
        r = APIResult(status, message, data)
        r.fields = ("status", "data")
    except (DataError, Exception):
        message = "Failed to query OXTS data!"
        r = APIResult(status, message, data)
        r.fields = ("status", "message", "data")
        app.logger.warning(message, exc_info=True)

    return r.json()


@api.route("/velo", defaults={"page": 1})
@api.route("/velo/<int:page>")
@login_required
def _velo(page: int):
    """Returns Velodyne data points"""
    status = False
    message = ''
    data = None
    start = (page - 1) * IPP
    stop = start + IPP
    # Filters
    filters = {}
    timestamp = request.args.get("timestamp")
    if timestamp is not None:
        timestamp = unquote(timestamp)
        try:
            datetime.fromisoformat(timestamp)
            filters["timestamp"] = timestamp
        except ValueError:
            message = "Invalid timestamp argument format!"
            r = APIResult(status, message)
            r.fields = ("status", "message")
            app.logger.warning(message, exc_info=True)
            return r.json()
    try:
        dt = DataTable(H5_FILE)
        rows = [row for row in dt.fetch_rows_as_dicts(start, stop, **filters)]
        data = {
            "oxts": rows,
            "total_pages": dt.rows_count // IPP  # FIXME: should return number of selected pages
        }
        status = True
        r = APIResult(status, message, data)
        r.fields = ("status", "data")
    except (DataError, Exception):
        message = "Failed to query Velodyne data!"
        r = APIResult(status, message, data)
        r.fields = ("status", "message", "data")
        app.logger.warning(message, exc_info=True)

    return r.json()
