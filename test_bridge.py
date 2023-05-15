import unittest
from bridge import *  # assuming the code you posted is in 'your_module.py'

class TestDBOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = get_connection()

    def test_create_db(self):
        create_db()
        cursor = self.connection.cursor()
        
        # Check that the tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        self.assertIn(('Comparisons',), tables)
        self.assertIn(('Objects',), tables)
        self.assertIn(('History',), tables)

    def test_new_comparison(self):
        comp_id = new_comparison("Test_Compare")
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Comparisons WHERE id=?", (comp_id,))
        comparison = cursor.fetchone()
        self.assertIsNotNone(comparison)
        self.assertEqual(comparison[1], "Test_Compare")

    def test_add_object_to_comparison(self):
        comp_id = new_comparison("Test_Compare")
        obj_id = add_object_to_comparison("Apple", comp_id)
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Objects WHERE id=?", (obj_id,))
        object = cursor.fetchone()
        self.assertIsNotNone(object)
        self.assertEqual(object[1], "Apple")

    def test_compare(self):
        comp_id = new_comparison("Test_Compare")
        obj1_id = add_object_to_comparison("Apple", comp_id)
        obj2_id = add_object_to_comparison("Banana", comp_id)
        compare(obj1_id, obj2_id, True)
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM History WHERE object1_id=? AND object2_id=?", (obj1_id, obj2_id))
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertTrue(result[3])

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

if __name__ == "__main__":
    unittest.main()