import unittest
from api import Scope, Search, Token

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
        
    def test_sandbox(self):
        t = Token(AUTH_ID, CLIENT_ID, [Scope.PUBLIC], sandbox=True)
        
        self.assertEquals( t._get_sandbox(), "sandbox.")
        
    def test_no_sandbox(self):
        t = Token(AUTH_ID, CLIENT_ID, [Scope.PUBLIC], sandbox=False)
        
        self.assertEquals( t._get_sandbox(), "")
        
    def test_token_passed_to_result(self):
        t = Token(AUTH_ID, CLIENT_ID, [Scope.PUBLIC], sandbox=True)
        
        expected = t.get_token()
        
        s = Search(t)
        results = s.new_search().keywords( "something" ).execute()
        
        got = results.get_token().get_token()
        
        self.assertEquals(expected, got)
        
    def test_token_passed_to_next_result(self):
        t = Token(AUTH_ID, CLIENT_ID, [Scope.PUBLIC], sandbox=True)

        s = Search(t)
        results = s.new_search().keywords( "playstation" ).execute()
        
        expected = results.get_token().get_token()
        
        results = results.next()
        
        got = results.get_token().get_token()
        
        self.assertEquals(expected, got)
        