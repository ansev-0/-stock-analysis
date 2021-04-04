from tweepy.api import API
from tweepy import OAuthHandler
from src.tools.path import get_financial_path
import json
import os

class TwitterAPIAuthJson(API):

    PATH_PREDENTIALS = 'twitter_credentials'
    DEFAULT_CREDENTIAL_NAME = 'twitter_app'
    TWITTER_CREDENTIALS = os.path.join(get_financial_path(), PATH_PREDENTIALS)
    _DEFAULT_CREDENTIALS_PATH = os.path.join(TWITTER_CREDENTIALS,
                                             f'{DEFAULT_CREDENTIAL_NAME}.json')

    def __init__(self, credentials=None, *args, **kwargs):
       
        self._credentials = self._auth_from_credentials(credentials) if credentials is not None \
            else self._default_credentials
        super().__init__(self._credentials, *args, **kwargs)


    @property
    def auth_credentials(self):
        return self._credentials

    @property
    def _default_credentials(self):
        return self._get_auth(self._load_json_credentials(self._DEFAULT_CREDENTIALS_PATH))

    def _auth_from_credentials(self, credentials):
        return self._get_auth(self._load_json_credentials(credentials) 
                              if isinstance(credentials, str) 
                              else self._validate_credentials(credentials))

    def _get_auth(self, dict_credentials):
        auth = OAuthHandler(
            **self._filter_credentials_by(dict_credentials, 
                                          ('consumer_key', 'consumer_secret', 'callback'))
        )
        auth.set_access_token(
            **self._filter_credentials_by(dict_credentials,
                                          ('key', 'secret'))
        )
        return auth

    @staticmethod
    def _validate_credentials(credentials):
        if not isinstance(credentials, dict):
            raise TypeError('Invalid Type, You must pass a path (str) or a dict crendentials')
        return credentials

    @staticmethod
    def _load_json_credentials(path):
        return json.load(open(path, 'r'))

    @staticmethod
    def _filter_credentials_by(credentials, key_filters):
        return {key : value 
                for key, value in credentials.items() 
                if any(key_filter == key 
                       for key_filter in key_filters)}

