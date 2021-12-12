import unittest
from api import Scope, Token

CREDENTIALS = ""

class Test_Scope(unittest.TestCase):
    def test_public(self):
        expected = "https://api.ebay.com/oauth/api_scope"
        self.assertEqual(Scope.PUBLIC, expected)

# class Test_API(unittest.TestCase):
#     def setUp(self):
#         self.key = api.Token(CREDENTIALS, api.Scope.PUBLIC)