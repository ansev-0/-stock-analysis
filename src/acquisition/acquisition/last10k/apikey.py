from requests.auth import AuthBase

class ApiKey(AuthBase):

    ''' Attaches Ocp-Apim-Subscription-Key to the given Request object. '''
    def __init__(self, apikey):
        self.apikey = apikey

    def __call__(self, request):
        ''' This function includes in headers the key required for the query. '''
        request.headers['Ocp-Apim-Subscription-Key'] = self.apikey
        return request