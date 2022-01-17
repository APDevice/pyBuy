""" contains constants for module """

class Scope:
    """ available scopes for token generations
    
    CONSTANTS
        PUBLIC : basic scope for access to search functions
    """
    
    # basic scope for access to search functions
    PUBLIC = "https://api.ebay.com/oauth/api_scope"
    
    INVENTORY = "https://api.ebay.com/oauth/api_scope/sell.inventory"  
    
    MARKETING = "https://api.ebay.com/oauth/api_scope/sell.marketing"
    
    ACCOUNT = "https://api.ebay.com/oauth/api_scope/sell.account"
    
    FULFILLMENT = "https://api.ebay.com/oauth/api_scope/sell.fulfillment"