#!/usr/bin/python3
"""Test for City view"""
import inspect
import json
import unittest

import pep8

from api.v1.app import app
from api.v1.views import cities
from models import storage, storage_t
from models.city import City
from models.state import State


class TestCityViewPEP8(unittest.TestCase):
    """Test Class for PEP8 conformance in City view"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.city_f = inspect.getmembers(cities, inspect.isfunction)

    def test_pep8_conformance_city_view(self):
        """Test that api/v1/views/cities.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["api/v1/views/cities.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_city_view(self):
        """Test that test_cities.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
                ["tests/test_api/test_v1/test_views/test_cities.py"]
                )
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_city_module_docstring(self):
        """Test for the cities.py module docstring"""
        self.assertIsNot(cities.__doc__, None, "cities.py needs a docstring")
        self.assertTrue(
                len(cities.__doc__) >= 1,
                "cities.py needs a docstring"
                )

    def test_city_func_docstrings(self):
        """Test for the presence of docstrings in City functions"""
        for func in self.city_f:
            self.assertIsNot(
                func[1].__doc__,
                None,
                "{:s} function needs a docstring".format(func[0])
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} function needs a docstring".format(func[0]),
            )


class TestCity(unittest.TestCase):
    """Test Class for city view"""

    def setUp(self):
        """Configure the app"""
        self.app = app.test_client()
        self.app.testing = True
        self.state = State(name="Test State")
        storage.new(self.state)
        storage.save()
        self.city = City(name="Test City", state_id=self.state.id)
        storage.new(self.city)
        storage.save()

    def tearDown(self):
        """Tear down test environment"""
        if storage_t == "db":
            storage.rollback()
        else:
            storage.reload()

    def test_get_cities(self):
        """Test GET all cities of a state"""
        response = self.app.get(f"/api/v1/states/{self.state.id}/cities")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_city(self):
        """Test GET a specific city by its ID"""
        city = City(name="Test City", state_id=self.state.id)
        storage.new(city)
        storage.save()
        if storage_t == "db":
            storage.reload()
        response = self.app.get(f"/api/v1/cities/{self.city.id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], self.city.id)

    def test_delete_city(self):
        """Test DELETE a specific city by its ID"""
        response = self.app.delete(f"/api/v1/cities/{self.city.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {})

    def test_create_city(self):
        """Test POST to create a city"""
        response = self.app.post(
            f"/api/v1/states/{self.state.id}/cities", json={"name": "New City"}
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "New City")

    def test_update_city(self):
        """Test PUT to update a city"""
        response = self.app.put(
            f"/api/v1/cities/{self.city.id}", json={"name": "Updated City"}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "Updated City")


if __name__ == "__main__":
    unittest.main()
