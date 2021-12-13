import requests
import json
from time import time
import logging as log
from base64 import b64encode

log.basicConfig(level=log.DEBUG)

class Scope:
    """ available scopes for token generations
    
    CONSTANTS
        PUBLIC : basic scope for access to search functions
    """
    
    # basic scope for access to search functions
    PUBLIC = "https://api.ebay.com/oauth/api_scope"


class Token:
    """ Token gets and buffers Oauth credential
    
    PARAMETERS
        app_id : App ID (aka Client ID) supplied by ebay
        cert_id : Cert ID (aka Client Secret) supplied by ebay
        scope : list of Scopes required for request (see Scope)
        sandbox : (optional) sets whether to use API in sandbox mode (default = True)
    """    
    __SANDBOX = "sandbox."
    
    def __init__(self, app_id: str,
                 cert_id: str,
                 scope: list,
                 sandbox = True) -> None:
        """ initilize Token instance """
        self.__sandbox_enabled = sandbox
        self.__key = app_id
        self.__secret = cert_id
        assert ( type(scope) is list ) or ( type(scope) is tuple ), "scope argument must be list or tuple"
        
        self.__scope = ' '.join(scope)
        
        log.debug(f"credentials: {self.__key}:{self.__secret}")
        log.debug(f"scope: {self.__scope}")
        
        # token buffer
        self.__token = None
        self.__last_retrieved = 0
    
    def Enable_sandbox(self) -> None:
        """ Enables sandbox mode """
        if not self.__sandbox_enabled:
            self.__token = None
        self.__sandbox_enabled = True

    def Disable_sandbox(self) -> None:
        """ Disables sandbox mode for token """
        if self.__sandbox_enabled:
            self.__token = None
        self.__sandbox_enabled = False

    def _get_sandbox(self):
        """ returns sandbox subdomain if sandbox is enabled, else returns empty string """
        return Token.__SANDBOX if self.__sandbox_enabled else ""

    def __auth(self) -> str:
        return 'Basic ' + b64encode((self.__key + ':' + self.__secret).encode()).decode()

    def get_token(self) -> dict:
        """ returns application access token """
        # if token doesn't already exist or it has expired, get new token
        if not self.__token or (self.__token['expires_in'] + self.__last_retrieved) < int(time()):
            url = f"https://api.{ self._get_sandbox() }ebay.com/identity/v1/oauth2/token"
            payload = f"grant_type=client_credentials&scope={ self.__scope }"
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Authorization': self.__auth()
            }
            
            response = requests.request("POST", url, data=payload, headers=headers)
            
            self.__last_retrieved = int(time())
            self.__token = json.loads(response.text)
        
        # raise error if query fails to return key
        if 'access_token' not in self.__token:
            raise PermissionError('access token invalid')
        
        return self.__token['access_token']
    
    def __str__(self) -> str:
        if self.__token:
            return self.__token['access_token']
        else:
            return "No valid token."

class Result:
    """ stores results of API request
    
    PARAMETERS
        json_data : raw json data from request
        token : authorization token
    """
    def __init__(self, json_data: str, token: Token) -> None:
        self.__raw_data = json_data
        self.__data = json.loads(json_data)
        self.__token = token
        
    def get_data(self) -> dict:
        """ returns result data as python dictionary """
        return self.__data
    
    def get_raw_data(self) -> str:
        """ returns raw response data """
        return self.__raw_data
    
    def __str__(self):
        return self.get_data()
    
    def has_next(self):
        """ returns true if there is a next page, else false """
        return "next" in self.__data
    
    def next(self):
        """ returns next page of results """
        if not self.has_next():
            raise KeyError("next page not available")
        
        url = self.__data["next"]
        headers = {
            'Authorization': f"Bearer {self._token.get_token()}"
        }
        response = requests.request("GET", url, headers=headers)
        
        return Result(response.text, self.__token)

    def has_previous(self):
        """ returns true if there is a previous page, else false """
        return "prev" in self.__data
    
    def previous(self):
        """ returns next page of results """
        if not self.has_next():
            raise KeyError("previous page not available")
        
        url = self.__data["prev"]
        headers = {
            'Authorization': f"Bearer {self._token.get_token()}"
        }
        response = requests.request("GET", url, headers=headers)
        
        return Result(response.text, self.__token)
    
class __Query: 
    """ abstract class for all query types """
    def __init__(self, token: Token) -> None:
        self._token = token

class Search(__Query):
    """ impliments search query """
    def __init__(self, token: Token) -> None:
        super().__init__(token)
        self.__args = {}

    def __str__(self):
        return self.__args
    
    def new_search(self) -> "Search":
        """ reset search object to begin new seach """
        self.__args.clear()
        self.__raw_data = None
        return self
    
    def keywords(self, *kwds: str, mode_or = False) -> "Search":
        """ adds keywords to search query """
        if mode_or:
            self.__args["q"] = f"({', '.join(kwds)})"
        else:
            self.__args["q"] = ' '.join(kwds)
        return self
        
    def execute(self) -> Result:
        """ returns results of search query """
        url = f"https://api.{ self._token._get_sandbox() }ebay.com/buy/browse/v1/item_summary/search?" + \
                "&".join(f"{k}={v}" for k, v in self.__args.items())
        headers = {
            'Authorization': f"Bearer {self._token.get_token()}"
        }
        
        response = requests.request("GET", url, headers=headers)
        
        return Result(response.text, self._token)
    
    



# url = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"

# payload = "apiKey=%3CREQUIRED%3E&SKU=%3CREQUIRED%3E"
# headers = {
#     'content-type': "application/x-www-form-urlencoded",
#     'Authorization': "Basic "
#     }

# response = requests.request("POST", url, data=payload, headers=headers)
# print("test")
# print(response.text)

