# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template

# from application.base import app

xhr = Blueprint("xhr", __name__, url_prefix="/xhr")


@xhr.route('/')
def _index():
    """"""
    return "OK"

