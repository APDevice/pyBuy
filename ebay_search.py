"""  """
from api import Scope, Token, Search
import json

KEYS_SOURCE = "keys.json"

def main():
    with open(KEYS_SOURCE, "r") as f:
        keys = json.load(f)
    
    t = Token(keys["App ID"], keys["Cert ID"], [Scope.PUBLIC])
    
    s = Search(t)
    
    results = s.new_search().keywords("playstation").execute()
    
    
    
if __name__ == '__main__':

    main()