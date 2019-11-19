from flask import Blueprint, jsonify

# from application.base import app
from application.data import get_oxts_as_dicts
from application.errors import DataError
from config import version, IPP


api = Blueprint("api", __name__, url_prefix="/api")


class APIResult:
    """"""
    def __init__(self, status: bool=True, message: str='', data: object=None):
        """"""
        self._status = status
        self._message = message
        self._data = data
        self._version = version

    @property
    def status(self) -> bool:
        """"""
        return  self._status

    @property
    def message(self) -> str:
        """"""
        return  self._message

    @property
    def data(self) -> object:
        """"""
        return  self._data

    def json(self) -> dict:
        """"""
        return jsonify({
            "status": self.status,
            "message": self.message,
            "data": self.data,
            "version": self._version,
        })

    def __str__(self):
        """"""
        return str(self.json())


@api.route('/')
def _index():
    """API root endpoint, return API details"""
    return APIResult(message="KITTI Flask Demo API").json()


@api.route("/oxts", defaults={"page": 1})
@api.route("/oxts/<int:page>")
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
