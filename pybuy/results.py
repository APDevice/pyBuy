""" contains classes for storing and parsing results """
import json

from requests import request

from .token import Token


class Result:
    """ stores results of API request
    
    PARAMETERS
        json_data : raw json data from request
        token : authorization token
    """
    def __init__(self,
                 json_data: str,
                 token: Token) -> None:
        self.__raw_data = json_data
        self.__data = json.loads(json_data)
        self.__token = token
        
    def get_token(self) -> Token:
        """ returns access token for this result """
        return self.__token
        
    def get_data(self) -> dict:
        """ returns result data as python dictionary """
        return self.__data
    
    def get_raw_data(self) -> str:
        """ returns raw response data """
        return self.__raw_data
    
    def __str__(self) -> str:
        return str(self.get_data())
    
    def has_next(self):
        """ returns true if there is a next page, else false """
        return "next" in self.get_data()
    
    def next(self) -> "Result":
        """ returns next page of results """
        if not self.has_next():
            raise KeyError("next page not available")
        
        url = self.__data["next"]
        headers = {
            'Authorization': f"Bearer {self.__token.get_token()}"
        }
        response = request("GET", url, headers=headers)
        
        return Result(response.text, self.__token)

    def has_previous(self) -> bool:
        """ returns true if there is a previous page, else false """
        return "prev" in self.get_data()
    
    def previous(self) -> "Result":
        """ returns next page of results """
        if not self.has_next():
            raise KeyError("previous page not available")
        
        url = self.__data["prev"]
        headers = {
            'Authorization': f"Bearer {self.__token.get_token()}"
        }
        response = request("GET", url, headers=headers)
        
        return Result(response.text, self.__token)
    
    def __iter__(self):
        """ iterate through results """
        return ResultIterator(self)


class ResultIterator():
    def __init__(self, result: Result) -> None:
        self.result = result
        
    def __next__(self):
        """ gets next result """
        if self.result.has_next():
            self.result = self.result.next()
        else:
            raise StopIteration