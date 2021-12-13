import unittest
from api import Scope, Token

AUTH_ID = "DylanLut-pyBuy-SBX-47ca6edf0-a73f32d9"
CLIENT_ID = "SBX-7ca6edf0bf2a-6443-4f6d-89e1-32be"

class Test_Scope(unittest.TestCase):
    def test_public(self):
        expected = "https://api.ebay.com/oauth/api_scope"
        self.assertEqual(Scope.PUBLIC, expected)



class Test_API(unittest.TestCase):
    def test_token_buffer(self):
        t = Token(AUTH_ID, CLIENT_ID, [Scope.PUBLIC])
        
        token_a = t.get_token()
        token_b = t.get_token()
        
        self.assertEquals(token_a, token_b)