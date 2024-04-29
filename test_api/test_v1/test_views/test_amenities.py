#!/usr/bin/python3
"""Test for Amenity view"""
import inspect
import json
import unittest

import pep8

from api.v1.app import app
from api.v1.views import amenities
from models import storage, storage_t
from models.amenity import Amenity


class TestAmenityViewPEP8(unittest.TestCase):
    """Test Class for PEP8 conformance in Amenity view"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.amenity_f = inspect.getmembers(amenities, inspect.isfunction)

    def test_pep8_conformance_amenity_view(self):
        """Test that api/v1/views/amenities.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["api/v1/views/amenities.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_amenity_view(self):
        """Test that test_amenities.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ["tests/test_api/test_v1/test_views/test_amenities.py"]
        )
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_amenity_module_docstring(self):
        """Test for the amenities.py module docstring"""
        self.assertIsNot(
                amenities.__doc__, None, "amenities.py needs a docstring"
                )
        self.assertTrue(
                len(amenities.__doc__) >= 1, "amenities.py needs a docstring"
                )

    def test_amenity_func_docstrings(self):
        """Test for the presence of docstrings in Amenity functions"""
        for func in self.amenity_f:
            self.assertIsNot(
                func[1].__doc__,
                None,
                "{:s} function needs a docstring".format(func[0])
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} function needs a docstring".format(func[0]),
            )


class TestAmenity(unittest.TestCase):
    """Test Class for amenity view"""

    def setUp(self):
        """Configure the app"""
        self.app = app.test_client()
        self.app.testing = True
        self.amenity = Amenity(name="Test Amenity")
        storage.new(self.amenity)
        storage.save()

    def tearDown(self):
        """Tear down test environment"""
        if storage_t == "db":
            storage.rollback()
        else:
            storage.reload()

    def test_get_amenities(self):
        """Test GET all amenities"""
        response = self.app.get("/api/v1/amenities")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_amenity(self):
        """Test GET a specific amenity by its ID"""
        amenity = Amenity(name="Test Amenity")
        storage.new(amenity)
        storage.save()
        if storage_t == "db":
            storage.reload()
        response = self.app.get(f"/api/v1/amenities/{self.amenity.id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], self.amenity.id)

    def test_delete_amenity(self):
        """Test DELETE a specific amenity by its ID"""
        response = self.app.delete(f"/api/v1/amenities/{self.amenity.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {})

    def test_create_amenity(self):
        """Test POST to create an amenity"""
        response = self.app.post(
                "/api/v1/amenities", json={"name": "New Amenity"}
                )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "New Amenity")

    def test_update_amenity(self):
        """Test PUT to update an amenity"""
        response = self.app.put(
            f"/api/v1/amenities/{self.amenity.id}",
            json={"name": "Updated Amenity"}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "Updated Amenity")


if __name__ == "__main__":
    unittest.main()
