#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
import sqlalchemy
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
from models import storage
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        cls.state = State(name="San Fransico")
        cls.city = City(name="Mexico", state_id=cls.state.id)
        storage.new(cls.state)
        storage.new(cls.city)
        storage.save()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        storage._DBStorage__session.expunge_all()
        storage.delete(cls.city)
        storage.delete(cls.state)
        storage.save()

    def setUp(self):
        """Refresh objects before each test"""
        self.state = storage._DBStorage__session.merge(self.state)
        self.city = storage._DBStorage__session.merge(self.city)

    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def test_get(self):
        """Test the get method"""
        retrieved_state = storage.get(State, self.state.id)
        self.assertEqual(retrieved_state, self.state)

    def test_count(self):
        """Test the count method"""
        self.assertEqual(storage.count(State), 1)
        self.assertEqual(storage.count(City), 1)

    def test_all_with_class(self):
        """Test the all method with class name argument"""
        states = storage.all(State)
        self.assertIn(self.state, states.values())

    def test_all_without_class(self):
        """Test the all method without class name argument"""
        objects = storage.all()
        self.assertIn(self.state, objects.values())
        self.assertIn(self.city, objects.values())

    def test_new(self):
        """Test the new method"""
        new_state = State(name="New State")
        storage.new(new_state)
        self.assertIn(new_state, storage.all(State).values())

    def test_delete(self):
        """Test the delete method"""
        new_state = State(name="Temporary State")
        storage.new(new_state)
        storage.save()
        storage.delete(new_state)
        self.assertNotIn(new_state, storage.all(State).values())

    def test_reload(self):
        """Test the reload method"""
        storage.reload()
        self.state = storage._DBStorage__session.merge(self.state)
        self.assertIn(self.state, storage.all(State).values())

    def test_close(self):
        """Test the close method"""
        storage.close()
        self.assertNotIn(self.state, storage._DBStorage__session)


if __name__ == "__main__":
    unittest.main()
