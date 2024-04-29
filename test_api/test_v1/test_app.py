#!/usr/bin/python3
"""Test Module for Flask app"""

import inspect
import os
import unittest

import pep8
from flask import Flask

from api.v1.app import app, not_found
from api.v1.views import app_views
from models import storage


class TestAppPEP8(unittest.TestCase):
    """Test Class for PEP8 conformance in Flask app"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.app_f = [
            ("teardown_appcontext", app.teardown_appcontext),
            ("not_found", not_found),
        ]

    def test_pep8_conformance_app(self):
        """Test that api/v1/app.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["api/v1/app.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_app(self):
        """Test that tests/test_api/test_v1/test_app.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["tests/test_api/test_v1/test_app.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_app_module_docstring(self):
        """Test for the app.py module docstring"""
        self.assertIsNot(app.__doc__, None, "app.py needs a docstring")
        self.assertTrue(len(app.__doc__) >= 1, "app.py needs a docstring")

    def test_app_func_docstrings(self):
        """Test for the presence of docstrings in app methods"""
        for func in self.app_f:
            self.assertIsNot(
                func[1].__doc__,
                None,
                "{:s} method needs a docstring".format(func[0])
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0]),
            )


class TestApp(unittest.TestCase):
    """Test Class for Flask app"""

    def setUp(self):
        """Configure the app"""
        self.app = app.test_client()
        self.app.testing = True

    def test_status(self):
        """Test status"""
        response = self.app.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "OK"})

    def test_404(self):
        """Test Error handling"""
        response = self.app.get("/api/v1/nonexistent_route")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_blueprint_registration(self):
        """Check Blueprint"""
        self.assertIn("app_views", self.app.application.blueprints)

    def test_tear_down(self):
        """Test teardown"""
        with self.app.application.app_context():
            storage.close()
            self.assertTrue(storage.is_closed)


if __name__ == "__main__":
    unittest.main()
