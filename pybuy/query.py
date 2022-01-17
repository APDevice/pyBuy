""" contains classes for querying data from api
"""
from abc import ABCMeta, abstractmethod
import csv

import requests

from .results import Result
from .token import Token
from typing import Optional, Tuple

class __Query(metaclass=ABCMeta): 
    """ abstract class for all query types """
    def __init__(self, token: Token) -> None:
        self._token = token
    
    @abstractmethod
    def execute(self):
        return

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
    
    def autocorrect(self,
                    active: bool) -> "Search":
        """ if True, adds autocorrect to search query """
        if active:
            self.__args["auto_correct"] = "KEYWORD"
        elif "auto_correct" in self.__args:
            self.__args.pop("auto_correct", None)
        
        return self
    
    def limit(self,
              cnt: int) -> "Search":
        """ set limit for number of results per page """
        self.__args["limit"] = cnt
        return self
    
    def sort(self,
             by: str,
             accending: bool = True) -> "Search":
        """[summary]
        
        Arguments:
            by (str): 
            
            accending (bool):
            
        Returns:
            (Search): 
        """
        
        if accending:
            self.__args["sort"] = by
        else:
            self.__args["sort"] = "-" + by
            
        return self
    
    def epid(self, epid: int) -> "Search":
        """ add eBay product identifier to search query """
        self.__args["epid"] = epid
        return self
    
    # TODO: impliment filtering
    # def filter(self,
    #            price: Optional[Tuple[int, int]] = None,
    #            ) -> "Search":
        
    #     return self
        
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
