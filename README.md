# pyBuy

*Work in progress*

The API for this project allows one to access the eBay developer API, query results, and transform them into a CSV file.

### Requirements
- Ebay developer account (see: https://developer.ebay.com)

### Installation

MacOS / Linux Terminal:
```
pip install https://github.com/APDevice/pyBuy/archive/refs/tags/v0.3.tar.gz
```
Windows Command Prompt:
```
py -m pip install https://github.com/APDevice/pyBuy/archive/refs/tags/v0.3.tar.gz
```
### API Usage
Before you can make any queries, you must first generate an application token. This action is performed using the Token class. 

```
from ebay_api import Scope, Token, Search

app_id = '' // use App ID supplied to developer account
cert_id = '' // use Cert ID supplied to developer account
scopes = [Scope.PUBLIC] // list of Scopes required for query

token = Token(app_id, cert_id, scopes)
```
From there you pass the token into the appropriate query.

The following demonstrates how to execute a simple search query. 
```
search = Search(token)

results = search.new_search().keywords(['LIST', 'OF', 'KEYWORDS']).execute()
```

Note that all queries start with the "new_search" method, and end with "execute". 'new_search' resets the query, while 'execute' makes the actual request. If you want to rerun the same request, simply use execute on the object. (eg search.execute())

**demonstration program 'search_ebay' requires valid Application keys in keys.json before it can run**

### Current Features:
- Oauth2 token generator
- Seach Query
    - Search By Keyword
    - Convert Results to csv
- Results
    - access queried data
