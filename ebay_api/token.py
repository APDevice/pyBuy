""" contains classes for token generation """

import json
import logging as log
from base64 import b64encode
from time import time

import requests


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
                 sandbox: bool = True) -> None:
        """ initilize Token instance """
        self.__sandbox_enabled = sandbox
        self.__key = app_id
        self.__secret = cert_id
        assert ( type(scope) is list ) or ( type(scope) is tuple ), "scope argument must be list or tuple"
        
        self.__scope = ' '.join(scope)
        
        # debug output
        log.debug(f"credentials: {self.__key}:{self.__secret}")
        log.debug(f"scope: {self.__scope}")
        
        # token buffer
        self.__token = None
        self.__last_retrieved = 0
    
    def enable_sandbox(self) -> None:
        """ Enables sandbox mode """
        if not self.__sandbox_enabled:
            self.__token = None
        self.__sandbox_enabled = True

    def disable_sandbox(self) -> None:
        """ Disables sandbox mode for token """
        if self.__sandbox_enabled:
            self.__token = None
        self.__sandbox_enabled = False

    def _get_sandbox(self) -> str:
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
        """ return token string if it exists """
        if self.__token:
            return self.__token['access_token']
        else:
            return "No valid token."
