import unittest
from ebay_api import Scope, Search, Token
import json

KEYS_SOURCE = "keys.json"
with open(KEYS_SOURCE, "r") as f:
        keys = json.load(f)

AUTH_ID = keys["App ID"] 
CLIENT_ID = keys["Cert ID"]

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
        