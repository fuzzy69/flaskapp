# -*- coding: UTF-8 -*-

from typing import Iterable

from flask import jsonify

from config import version


class APIResult:
    """API result data container"""
    FIELDS = ("status", "message", "data", "version")

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
        self._fields = []

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

    @property
    def fields(self) -> list:
        """Returns list of JSON key fields"""
        return self._fields

    @fields.setter
    def fields(self, fields: Iterable):
        """Sets available response JSON key fields"""
        self._fields = list(filter(lambda x: x in APIResult.FIELDS, fields))

    def json(self) -> dict:
        """Returns all result fields as JSON object"""
        data = {}
        for field in self.fields:
            if "_" + field in dir(self):
                data[field] = getattr(self, "_" + field)

        return jsonify(data)

    def __str__(self):
        """Overridden"""
        return str(self.json())
