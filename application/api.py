# -*- coding: UTF-8 -*-

from flask import Blueprint, jsonify
from flask_login import login_required

from application.data import get_oxts_as_dicts
from application.errors import DataError
from config import version, IPP


api = Blueprint("api", __name__, url_prefix="/api")


class APIResult:
    """API result data container"""
    def __init__(self, status: bool=True, message: str='', data: object=None):
        """
        :param bool status: result status
        :param str message: message text, mostly for error descriptions
        :param object data: result data
        """
        self._status = status
        self._message = message
        self._data = data
        self._version = version

    @property
    def status(self) -> bool:
        """Returns results status True if succeeded otherwise False"""
        return  self._status

    @property
    def message(self) -> str:
        """Returns message string"""
        return  self._message

    @property
    def data(self) -> object:
        """Returns result data or None"""
        return  self._data

    def json(self) -> dict:
        """Returns all result fields as JSON object"""
        return jsonify({
            "status": self.status,
            "message": self.message,
            "data": self.data,
            "version": self._version,
        })

    def __str__(self):
        """Overridden"""
        return str(self.json())


@api.route('/')
@login_required
def _index():
    """API root endpoint, return API details"""
    return APIResult(message="KITTI Flask Demo API").json()


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
    try:
        rows, total_rows_count = get_oxts_as_dicts(start, stop)
        data = {
            "oxts": rows,
            "total_pages": total_rows_count // IPP
        }
        status = True
    except (DataError, Exception):
        message = "Failed to query OXTS data!"
        # app.logger.warning(message, exc_info=True)

    return APIResult(status, message, data).json()
