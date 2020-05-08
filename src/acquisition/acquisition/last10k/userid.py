from requests.auth import AuthBase

class UserId(AuthBase):
    
    """Attaches Ocp-Apim-Subscription-Key to the given Request object."""
    def __init__(self, user_id):
        self.user_id = user_id

    def __call__(self, request):
        ''' This function includes in headers the key and user value required for the query. '''
        request.headers['Ocp-Apim-Subscription-Key'] = self.user_id
        return request