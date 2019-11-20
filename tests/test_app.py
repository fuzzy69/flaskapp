# -*- coding: UTF-8 -*-

from logging import DEBUG, captureWarnings, getLogger, StreamHandler
from sys import stdout
from unittest import TestCase, main

from application.base import app, db


logger = getLogger("test")
logger.setLevel(DEBUG)
stream_handler = StreamHandler(stdout)
logger.addHandler(stream_handler)
captureWarnings(True)


class TestApp(TestCase):
    """Tests Flask app methods"""

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLE"] = False
        app.config["DEBUG"] = False
        # app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_index(self):
        """Tests home page"""
        r = self.app.get('/', follow_redirects=True)
        self.assertEqual(r.status_code, 200)

    def test_404(self):
        """Tests page not found"""
        r = self.app.get("/dummy", follow_redirects=True)
        self.assertEqual(r.status_code, 404)

    def test_login(self):
        """Tests user login"""
        # Valid user
        r = self.app.post("/login", data=dict(username="demo", password="demo"), follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Sign out", r.data)
        # Invalid user
        r = self.app.post("/login", data=dict(username="dummy", password="dummy"), follow_redirects=True)
        self.assertIn(b"Please enter valid username/password!", r.data)


if __name__ == "__main__":
    main()
