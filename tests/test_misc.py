import unittest
from pybuy import Scope


class Test_Scope(unittest.TestCase):
    def test_public(self):
        expected = "https://api.ebay.com/oauth/api_scope"
        self.assertEqual(Scope.PUBLIC, expected)

