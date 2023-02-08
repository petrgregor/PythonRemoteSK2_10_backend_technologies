from django.test import TestCase
from django.db.utils import IntegrityError

# Create your tests here.
class ExampleTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true")
        self.assertFalse(False)

    def test_add(self):
        print("Method: test_add")
        self.assertEqual(1+1, 2)


