from tweepy.api import API
from src.tools.path import get_financial_path
import tweepy
import json
import os

class TwitterAPIAuthJson(API):
    
    _FINANCIAL_PATH = get_financial_path()
    _DEFAULT_CREDENTIALS_PATH = os.path.join(_FINANCIAL_PATH, 
                                             'twitter_app.json')

    def __init__(self, credentials=None, *args, **kwargs):
        self._auth = self._auth_from_credentials(credentials) \
            if credentials is not None else self._default_credentials
        super().__init__(self._auth, *args, **kwargs)

    @property
    def _default_credentials(self):
        return self._get_auth(self._load_json_credentials(self._DEFAULT_CREDENTIALS_PATH))

    def _auth_from_credentials(self, credentials):
        return self._get_auth(self._load_json_credentials(credentials) 
                              if isinstance(credentials, str) 
                              else self._validate_credentials(credentials))

    def _get_auth(self, dict_credentials):
        auth = tweepy.OAuthHandler(
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

