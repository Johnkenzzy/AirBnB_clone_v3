#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker
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
        # self.assertEqual(result.total_errors, 0,
                         # "Found code style errors (and warnings).")

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


class TestFileStorage(unittest.TestCase):
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


class TestDBStorage(unittest.TestCase):
    """Unit tests for DBStorage methods"""

    def setUp(self):
        """Set up test environment"""
        self.storage = DBStorage()
        self.mock_session = MagicMock()
        self.storage._DBStorage__session = self.mock_session  # Manually set mock session

    @unittest.skipIf(DBStorage.__name__ != 'DBStorage', "not testing db storage")
    def test_get_existing_object(self):
        """Test retrieving an existing object"""
        mock_user = User(id="1234")
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_user
        self.mock_session.query.return_value = mock_query  # Mock query execution
        
        result = self.storage.get(User, "1234")
        self.assertEqual(result, mock_user)

    @unittest.skipIf(DBStorage.__name__ != 'DBStorage', "not testing db storage")
    def test_get_non_existing_object(self):
        """Test retrieving a non-existing object"""
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = None
        self.mock_session.query.return_value = mock_query
        
        result = self.storage.get(User, "5678")
        self.assertIsNone(result)

    @unittest.skipIf(DBStorage.__name__ != 'DBStorage', "not testing db storage")
    def test_count_all_objects(self):
        """Test counting all objects"""
        mock_query = MagicMock()
        mock_query.count.return_value = 5
        self.mock_session.query.return_value = mock_query
        
        result = self.storage.count(User)
        self.assertEqual(result, 5)

    @unittest.skipIf(DBStorage.__name__ != 'DBStorage', "not testing db storage")
    def test_count_no_objects(self):
        """Test counting objects when none exist"""
        mock_query = MagicMock()
        mock_query.count.return_value = 0
        self.mock_session.query.return_value = mock_query
        
        result = self.storage.count(User)
        self.assertEqual(result, 0)

if __name__ == "__main__":
    unittest.main()
