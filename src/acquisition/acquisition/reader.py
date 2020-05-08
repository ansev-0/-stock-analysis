from src.request_api import RequestsApi
from src.view.acquisition.reader import ReaderShowStatus
import requests

class Reader:
    def __init__(self, base_url, **kwargs):
        self.request = RequestsApi(base_url=base_url, **kwargs)
        self.show_status = ReaderShowStatus()
    def read(self, query, **kwargs):
            try:
                self.show_status.notify_try_connect(query)
                response = self.request.get(params=query, **kwargs)
                self.show_status.notify_not_error()
                return response
                
            except requests.exceptions.RequestException as error:
                self.show_status.notify_error()
                return error
