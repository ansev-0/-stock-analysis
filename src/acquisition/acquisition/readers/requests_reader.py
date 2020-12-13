from src.request_api import RequestsApi
from src.acquisition.acquisition.readers.reader import Reader
import requests

class RequestsReader(Reader):

    def __init__(self, base_url='', **kwargs):
        self.request = RequestsApi(base_url=base_url, **kwargs)


    @property
    def base_url(self):
        return self.request.base_url

    @base_url.setter
    def base_url(self, base_url):
        self.request.base_url = base_url

    def __call__(self, query, **kwargs):
        
        try:
            self._show_status.notify_try_connect(query)
            response = self.request.get(params=query, **kwargs)
        
        except requests.exceptions.RequestException as error:
            self._show_status.notify_error()
            return error

        else:
            self.show_status.notify_not_error()
            return response.json()
