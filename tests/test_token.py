import unittest
from pybuy import Scope, Search, Token
import json
import os

keys = dict()
if "EBAY_APP_ID" in os.environ:
    AUTH_ID = os.environ["EBAY_APP_ID"]
    CLIENT_ID = os.environ["EBAY_CERT_ID"]
else:
    KEYS_SOURCE = "keys.json"
    with open(KEYS_SOURCE, "r") as f:
        keys = json.load(f)

    AUTH_ID = keys["App ID"] 
    CLIENT_ID = keys["Cert ID"]

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
        results = (s.new_search()
                   .keywords( "playstation" )
                   .execute())
        
        got = results.get_token().get_token()
        
        self.assertEquals(expected, got)
        
    def test_token_passed_to_next_result(self):
        t = Token(AUTH_ID, CLIENT_ID, [Scope.PUBLIC], sandbox=True)

        s = Search(t)
        results = (s.new_search()
                   .keywords( "playstation", "xbox", mode_or=True)
                   .limit(10)
                   .execute())
        
        expected = results.get_token().get_token()
        
        results = results.next()
        
        got = results.get_token().get_token()
        
        self.assertEquals(expected, got)
        