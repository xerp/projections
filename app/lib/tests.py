import unittest
import helpers

class DatabaseTest(unittest.TestCase):

    def test_check_database_exists(self):
        self.assertFalse(helpers.exists_user_database())

    def test_create_database(self):
        helpers.create_user_database()

        self.assertTrue(helpers.exists_user_database())
