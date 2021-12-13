"""  """
from api import Scope, Token, Search
import json
import pandas as pd

def main():
    with open("keys.json", "r") as f:
        keys = json.load(f)
    
    t = Token(keys["App ID"], keys["Cert ID"], [Scope.PUBLIC])
    
    s = Search(t)
    
    results = s.new_search().keywords("playstation").execute()
    
    df = pd.json_normalize(results.get_data()["itemSummaries"])
    
    print(df)
    
if __name__ == '__main__':

    main()