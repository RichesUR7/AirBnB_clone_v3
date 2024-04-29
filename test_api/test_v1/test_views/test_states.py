i#!/usr/bin/python3
"""Test for State view"""
import inspect
import unittest

import pep8
from flask import json

from api.v1.app import app
from api.v1.views import states
from models import storage, storage_t
from models.state import State


class TestStateViewPEP8(unittest.TestCase):
    """Test Class for PEP8 conformance in State view"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.state_f = inspect.getmembers(states, inspect.isfunction)

    def test_pep8_conformance_state_view(self):
        """Test that api/v1/views/states.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["api/v1/views/states.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_state_view(self):
        """Test that test_states.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
                ["tests/test_api/test_v1/test_views/test_states.py"]
                )
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_state_module_docstring(self):
        """Test for the states.py module docstring"""
        self.assertIsNot(states.__doc__, None, "states.py needs a docstring")
        self.assertTrue(
                len(states.__doc__) >= 1,
                "states.py needs a docstring"
                )

    def test_state_func_docstrings(self):
        """Test for the presence of docstrings in State functions"""
        for func in self.state_f:
            self.assertIsNot(
                func[1].__doc__,
                None,
                "{:s} function needs a docstring".format(func[0])
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} function needs a docstring".format(func[0]),
            )


class TestStates(unittest.TestCase):
    """Test Class for states view"""

    def setUp(self):
        """Configure the app"""
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        """Tear down test environment"""
        if storage_t == "db":
            storage.rollback()
        else:
            storage.reload()

    def test_get_states(self):
        """Test GET all states"""
        response = self.app.get("/api/v1/states")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        for state in data:
            self.assertIsInstance(state, dict)

    def test_get_state(self):
        """Test GET a specific state"""
        state = State(name="Test State")
        storage.new(state)
        storage.save()
        storage.reload()
        response = self.app.get(f"/api/v1/states/{state.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], state.id)

    def test_delete_state(self):
        """Test DELETE a specific state"""
        state = State(name="Test State")
        storage.new(state)
        storage.save()
        response = self.app.delete(f"/api/v1/states/{state.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {})

    def test_create_state(self):
        """Test POST to create a state"""
        response = self.app.post("/api/v1/states", json={"name": "New State"})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "New State")

    def test_update_state(self):
        """Test PUT to update a state"""
        state = State(name="Test State")
        storage.new(state)
        storage.save()
        response = self.app.put(
            f"/api/v1/states/{state.id}", json={"name": "Updated State"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "Updated State")


if __name__ == "__main__":
    unittest.main()
