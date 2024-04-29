#!/usr/bin/python3
"""Test Module for index view"""
import inspect
import unittest

import pep8
from flask import json

from api.v1.app import app
from api.v1.views import index
from api.v1.views.index import MODEL_CLASSES


class TestIndexViewPEP8(unittest.TestCase):
    """Test Class for PEP8 conformance in Index view"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.index_f = inspect.getmembers(index, inspect.isfunction)

    def test_pep8_conformance_index_view(self):
        """Test that api/v1/views/index.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["api/v1/views/index.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_index_view(self):
        """Test that test_index.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
                ["tests/test_api/test_v1/test_views/test_index.py"]
                )
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_index_module_docstring(self):
        """Test for the index.py module docstring"""
        self.assertIsNot(index.__doc__, None, "index.py needs a docstring")
        self.assertTrue(len(index.__doc__) >= 1, "index.py needs a docstring")

    def test_index_func_docstrings(self):
        """Test for the presence of docstrings in Index functions"""
        for func in self.index_f:
            self.assertIsNot(
                func[1].__doc__,
                None,
                "{:s} function needs a docstring".format(func[0])
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} function needs a docstring".format(func[0]),
            )


class TestIndex(unittest.TestCase):
    """Test Class for index view"""

    def setUp(self):
        """Configure the app"""
        self.app = app.test_client()
        self.app.testing = True

    def test_status(self):
        """Test status route"""
        response = self.app.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "OK"})

    def test_get_storage_stats(self):
        """Test stats route"""
        response = self.app.get("/api/v1/stats")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(set(data.keys()), set(MODEL_CLASSES.keys()))
        for key, value in data.items():
            self.assertIsInstance(value, int)
            self.assertGreaterEqual(value, 0)


if __name__ == "__main__":
    unittest.main()
