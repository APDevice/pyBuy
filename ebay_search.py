""" ebay API usage example """
from pybuy import Scope, Token, Search
import json
import sys
import time
import logging as log
from pprint import pprint

KEYS_SOURCE = "keys_test.json"

log.basicConfig(level=log.DEBUG)
 

def main():
    """ main program """
    if len(sys.argv) < 2:
        print(f"USAGE : {sys.argv[0]} <space seperated keywords>")
        exit()
        
    # load application keys
    with open(KEYS_SOURCE, "r") as f:
        keys = json.load(f)
    
    t = Token(keys["App ID"], keys["Cert ID"], [Scope.PUBLIC])
    
    s = Search(t)
    
    results = s.new_search().keywords( *sys.argv[1:] ).execute()
    # pprint(results.get_data())
    Search.to_csv("search.csv", results)
    
    Search.to_json("search.json", results, human_readable=True)
    
    pages = 0
    while results.has_next() and pages < 10:
        time.sleep(0.5)
        pages += 1
        results = results.next()
        Search.to_csv("search.csv", results, append = True)
        

if __name__ == '__main__':

    main()