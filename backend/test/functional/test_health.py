import unittest

from src.ase import app
from src.ase.app import API_ROOT


class TestHealth(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get(API_ROOT + "/health")
        self.assertEqual(response.status_code, 200)

    def test_content_type(self):
        tester = app.test_client(self)
        response = tester.get(API_ROOT + "/health")
        self.assertEqual(response.content_type, "application/json")


if __name__ == "__main__":
    unittest.main()
