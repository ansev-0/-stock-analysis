from src.acquisition.acquisition.twitter_acquisition.search import TwitterSearchPopular
from src.acquisition.to_database.select_db.twitter_select import TwitterSelectDbToUpdate
from src.acquisition.to_database.twitter_db.flatten_response import FlattenResponse
from src.acquisition.to_database.twitter_db.searchs_asset.update import UpdateSearchAsset
from tweepy.error import RateLimitError
from pandas import to_datetime
from datetime import datetime
from tweepy.models import SearchResults
from collections import defaultdict
import os
from datetime import datetime

class TwitterSearchToDataBases:
    
    twitter_search = TwitterSearchPopular()
    _twitter_select_db = TwitterSelectDbToUpdate()
    _decode_map = ('id', 'created_at', 'full_text', 
                   'retweet_count', 'favorite_count', 
                   'lang',
                   {'user' : ('screen_name', 'name', 'followers_count', 
                              'friends_count', 'favourites_count')})
    
    _flatten_response = FlattenResponse(_decode_map)
    
    _NAME_CREDENTIALS = 'twitter_s'
    _LIMIT_CREDENTIALS = 5

    def __init__(self, crendential_index=-1):
        self._crendential_index = crendential_index
        self._api_status = {}


    def __call__(self, *args, **kwargs):
        # make request
        response = self._make_request(*args, **kwargs)
        #check bad response
        if not response or isinstance(response, str):
            output = dict(self._api_status), response
            #reset dict _api_status
            self._api_status = {}
            return output

        l_response = []
        for obj_response in response:
            #update databases
            self._update(
                self._flatten_response.one(obj_response),
                self._twitter_select_db(obj_response.full_text)
            )
            #save response in list
            l_response.append(obj_response)
        # get output
        output = dict(self._api_status), l_response
        #reset dict _api_status
        self._api_status = {}

        return output
        

    def _update(self, flatten_response, list_to_update):
        for collection_to_update in list_to_update:
            dict_to_update = self._correct_format_fields(flatten_response)
            UpdateSearchAsset(collection_to_update).one(self._get_day_id(flatten_response['created_at']), 
                                                        {dict_to_update['created_at'] : {key: value 
                                                                                         for key, value in dict_to_update.items()
                                                                                         if key != 'created_at'}})

    def _make_request(self, *args, **kwargs):

        try:
            output = self.twitter_search.get_full_text(*args, **kwargs)
            self._api_status[self._current_key_status] = True
            return output

        except RateLimitError:
            if self._update_credentials():
                return self._make_request(*args, **kwargs)
            else:
                 return []
        except Exception as error:
            str_error = str(error)

            if self._update_credentials(str_error):
                return self._make_request(*args, **kwargs)
            else:
                 return str(str_error)

    @property
    def _current_key_status(self):
        return f'{self._NAME_CREDENTIALS}{self._crendential_index}' \
                         if self._crendential_index >= 0 \
                         else self.twitter_search.DEFAULT_CREDENTIAL_NAME

    def _update_credentials(self, error=None):
        #put saturated
        self._api_status[self._current_key_status] = error if error is None else False
        
        self._crendential_index += 1
        if self._crendential_index > self._LIMIT_CREDENTIALS:
            return False
        self.twitter_search.auth = os.path.join(self.twitter_search.TWITTER_CREDENTIALS, 
                                                 f'{self._NAME_CREDENTIALS}{self._crendential_index}')
        return True                                          

    @staticmethod
    def _correct_format_fields(flatten_response):
        return {field : (str(value) if isinstance(value, datetime) else value) 
                for field, value in flatten_response.items()}

    @staticmethod
    def _get_day_id(created_at):
        return to_datetime(created_at.date())
