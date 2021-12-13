""" contains classes for querying data from api
"""
import requests
import csv
from .token import Token
from .results import Result

# class Scope:
#     """ available scopes for token generations
    
#     CONSTANTS
#         PUBLIC : basic scope for access to search functions
#     """
    
#     # basic scope for access to search functions
#     PUBLIC = "https://api.ebay.com/oauth/api_scope"

# class Result:
#     """ stores results of API request
    
#     PARAMETERS
#         json_data : raw json data from request
#         token : authorization token
#     """
#     def __init__(self,
#                  json_data: str,
#                  token: Token) -> None:
#         self.__raw_data = json_data
#         self.__data = json.loads(json_data)
#         self.__token = token
        
#     def get_token(self) -> Token:
#         """ returns access token for this result """
#         return self.__token
        
#     def get_data(self) -> dict:
#         """ returns result data as python dictionary """
#         return self.__data
    
#     def get_raw_data(self) -> str:
#         """ returns raw response data """
#         return self.__raw_data
    
#     def __str__(self) -> str:
#         return str(self.get_data())
    
#     def has_next(self):
#         """ returns true if there is a next page, else false """
#         return self.__data["total"] > (self.__data["limit"] + self.__data["offset"])
    
#     def next(self) -> "Result":
#         """ returns next page of results """
#         if not self.has_next():
#             raise KeyError("next page not available")
        
#         url = self.__data["next"]
#         headers = {
#             'Authorization': f"Bearer {self.__token.get_token()}"
#         }
#         response = requests.request("GET", url, headers=headers)
        
#         return Result(response.text, self.__token)

#     def has_previous(self) -> bool:
#         """ returns true if there is a previous page, else false """
#         return self.__data["offset"] > 0
    
#     def previous(self) -> "Result":
#         """ returns next page of results """
#         if not self.has_next():
#             raise KeyError("previous page not available")
        
#         url = self.__data["prev"]
#         headers = {
#             'Authorization': f"Bearer {self.__token.get_token()}"
#         }
#         response = requests.request("GET", url, headers=headers)
        
#         return Result(response.text, self.__token)
    
class __Query: 
    """ abstract class for all query types """
    def __init__(self, token: Token) -> None:
        self._token = token

class Search(__Query):
    """ impliments search query 
    
    PARAMETER
        Token : a valid Oauth token
    """
    def __init__(self,
                 token: Token) -> None:
        super().__init__(token)
        self.__args = {}

    def __str__(self):
        return self.__args
    
    def new_search(self) -> "Search":
        """ reset search object to begin new seach """
        self.__args.clear()
        return self
    
    def keywords(self,
                 *kwds: str,
                 mode_or: bool = False) -> "Search":
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

    @staticmethod
    def to_csv(file_name: str,
               result: Result,
               append: bool = False) -> None:
        """ converts Result to csv file """
        items = result.get_data()["itemSummaries"]
        
        columns = ("itemId", "title", "price", "adultOnly", "itemLocation", "itemWebUrl")
        
        with open(file_name, "a" if append else "w") as f:
            writer = csv.writer(f)
            
            # write header
            writer.writerow(("id", "title", "price", "adult_only", "location", "url"))
            
            # loop through items in query
            for item in items:
                row = []
                for col in columns:
                    if col == "itemLocation": 
                        # combine values of item location
                        location = ", ".join(loc for loc in item["itemLocation"])
                        row.append( location )
                    elif col == "price":
                        # join price with currency
                        price = item['price']['value'] + item['price']['currency']
                        row.append( price )
                    else:
                        row.append( item[col] )
                writer.writerow( row )