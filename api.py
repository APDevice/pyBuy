import requests
import json
from time import time
import logging as log
from base64 import b64encode

log.basicConfig(level=log.DEBUG)

class Scope:
    """ available scopes for token generations """
    PUBLIC = "https://api.ebay.com/oauth/api_scope" #access public data


class Token:
    """ Token gets and buffers Oauth credential
    
    Methods
        get_token() -> dict
            gets token. If token already exists and has not expired, will return that.
            Otherwise requests new token from server
    """    
    __sandbox = "sandbox."
    
    def __init__(self, auth_id: str,
                 client_id: str,
                 scope: list) -> None:
        """ initilize Token instance """
        self.__key = auth_id
        self.__secret = client_id
        assert ( type(scope) is list ) or ( type(scope) is tuple ), "scope argument must be list or tuple"
        
        self.__scope = ' '.join(scope)
        
        log.debug(f"credentials: {self.__key}:{self.__secret}")
        log.debug(f"scope: {self.__scope}")
        
        # token buffer
        self.__token = None
        self.__last_retrieved = 0
    
    @classmethod
    def EnableSandbox(cls) -> None:
        """ Enables sandbox mode """
        cls.__sandbox = "sandbox."

    @classmethod
    def DisableSandbox(cls) -> None:
        """ Disables sandbox mode """
        cls.__sandbox  = ""

    def __auth(self) -> str:
        return 'Basic ' + b64encode((self.__key + ':' + self.__secret).encode()).decode()

    def get_token(self) -> dict:
        """ returns application access token """
        # if token doesn't already exist or it has expired, get new token
        if not self.__token or (self.__token['expires_in'] + self.__last_retrieved) < int(time()):
            url = f"https://api.{ Token.__sandbox }ebay.com/identity/v1/oauth2/token"
            payload = f"grant_type=client_credentials&scope={ self.__scope }"
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Authorization': self.__auth()
            }
            
            response = requests.request("POST", url, data=payload, headers=headers)
            
            self.__last_retrieved = int(time())
            self.__token = json.loads(response.text)
        
        return self.__token
    
    def __str__(self) -> str:
        if self.__token:
            return self.__token['access_token']
        else:
            return "No valid token."

# class Search(token)
#     def search(token: Token):
#         url = ""
#         payload = ""
#         header = {
            
#         }
        
        



# url = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"

# payload = "apiKey=%3CREQUIRED%3E&SKU=%3CREQUIRED%3E"
# headers = {
#     'content-type': "application/x-www-form-urlencoded",
#     'Authorization': "Basic "
#     }

# response = requests.request("POST", url, data=payload, headers=headers)
# print("test")
# print(response.text)

