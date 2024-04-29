#!/usr/bin/python3
"""Test for User view"""
import inspect
import json
import unittest

import pep8

from api.v1.app import app
from api.v1.views import users
from models import storage, storage_t
from models.user import User


class TestUserViewPEP8(unittest.TestCase):
    """Test Class for PEP8 conformance in User view"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.user_f = inspect.getmembers(users, inspect.isfunction)

    def test_pep8_conformance_user_view(self):
        """Test that api/v1/views/users.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["api/v1/views/users.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_user_view(self):
        """Test that test_users.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
                ["tests/test_api/test_v1/test_views/test_users.py"]
                )
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_user_module_docstring(self):
        """Test for the users.py module docstring"""
        self.assertIsNot(users.__doc__, None, "users.py needs a docstring")
        self.assertTrue(len(users.__doc__) >= 1, "users.py needs a docstring")

    def test_user_func_docstrings(self):
        """Test for the presence of docstrings in User functions"""
        for func in self.user_f:
            self.assertIsNot(
                func[1].__doc__,
                None,
                "{:s} function needs a docstring".format(func[0])
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} function needs a docstring".format(func[0]),
            )


class TestUser(unittest.TestCase):
    """Test Class for user view"""

    def setUp(self):
        """Configure the app"""
        self.app = app.test_client()
        self.app.testing = True
        self.user = User(email="test@test.com", password="test")
        storage.new(self.user)
        storage.save()

    def tearDown(self):
        """Tear down test environment"""
        if storage_t == "db":
            storage.rollback()
        else:
            storage.reload()

    def test_get_users(self):
        """Test GET all users"""
        response = self.app.get("/api/v1/users")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_user(self):
        """Test GET a specific user by its ID"""
        user = User(email="test@test.com", password="test")
        storage.new(user)
        storage.save()
        if storage_t == "db":
            storage.reload()
        response = self.app.get(f"/api/v1/users/{self.user.id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], self.user.id)

    def test_delete_user(self):
        """Test DELETE a specific user by its ID"""
        response = self.app.delete(f"/api/v1/users/{self.user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {})

    def test_create_user(self):
        """Test POST to create a user"""
        response = self.app.post(
            "/api/v1/users", json={"email": "new@test.com", "password": "new"}
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["email"], "new@test.com")

    def test_update_user(self):
        """Test PUT to update a user"""
        user = User(email="test@test.com", password="test")
        storage.new(user)
        storage.save()
        if storage_t == "db":
            storage.reload()
        response = self.app.put(
            f"/api/v1/users/{self.user.id}", json={"password": "updated"}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], self.user.id)


if __name__ == "__main__":
    unittest.main()
