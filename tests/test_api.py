# -*- coding: UTF-8 -*-

from json import loads
from logging import DEBUG, captureWarnings, getLogger, StreamHandler
from sys import stdout
from unittest import TestCase, main

from application.base import app, db


logger = getLogger("test")
logger.setLevel(DEBUG)
stream_handler = StreamHandler(stdout)
logger.addHandler(stream_handler)
captureWarnings(True)


class TestApi(TestCase):
    """Tests Flask app methods"""

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLE"] = False
        app.config["DEBUG"] = False
        # app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
        self.app = app.test_client()
        self.app.environ_base["HTTP_AUTHORIZATION"] = "Bearer demo:ZGVtb3Rva2Vu"
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_token(self):
        """Tests auth header token"""
        # Invalid token
        self.app.environ_base["HTTP_AUTHORIZATION"] = "Bearer demo:ZGVtb3Rva2Vf"
        r = self.app.get("/api", follow_redirects=True)
        json_data = loads(r.data)
        self.assertEqual(r.status_code, 401)
        # Valid token
        self.app.environ_base["HTTP_AUTHORIZATION"] = "Bearer demo:ZGVtb3Rva2Vu"
        r = self.app.get("/api", follow_redirects=True)
        json_data = loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(json_data.get("status"))


if __name__ == "__main__":
    main()
