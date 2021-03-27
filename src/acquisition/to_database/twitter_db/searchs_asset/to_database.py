from src.acquisition.acquisition.twitter_acquisition.search import TwitterSearchPopular
from src.acquisition.to_database.select_db.twitter_select import TwitterSelectDbToUpdate
from src.acquisition.to_database.twitter_db.flatten_response import FlattenResponse
from src.acquisition.to_database.twitter_db.searchs_asset.update import UpdateSearchAsset
from tweepy.error import RateLimitError
from pandas import to_datetime
from datetime import datetime
from tweepy.models import SearchResults
import os

class TwitterSearchToDataBases:

    _twitter_search = TwitterSearchPopular()
    _twitter_select_db = TwitterSelectDbToUpdate()
    _decode_map = ('id', 'created_at', 'full_text', 
                   'retweet_count', 'favorite_count', 
                   'lang',
                   {'user' : ('screen_name', 'name', 'followers_count', 
                              'friends_count', 'favourites_count')})
    
    _flatten_response = FlattenResponse(_decode_map)
    _NAME_CREDENTIALS = 'twitter_s'
    _LIMIT_CREDENTIALS = 2

    def __init__(self):
        self._crendential_index = -1

    def __call__(self, *args, **kwargs):
        # make request
        response = self._make_request(*args, **kwargs)
        #check bad response
        if not response or isinstance(response, str):
            return response

        l_response = []
        for obj_response in response:
            #update databases
            self._update(
                self._flatten_response.one(obj_response),
                self._twitter_select_db(obj_response.full_text)
            )
            #save response in list
            l_response.append(obj_response)

        return l_response

    def _update(self, flatten_response, list_to_update):
        for collection_to_update in list_to_update:
            dict_to_update = self._correct_format_fields(flatten_response)
            UpdateSearchAsset(collection_to_update).one(self._get_day_id(flatten_response['created_at']), 
                                                        {dict_to_update['created_at'] : {key: value 
                                                                                         for key, value in dict_to_update.items()
                                                                                         if key != 'created_at'}})

    def _make_request(self, *args, **kwargs):

        try:
            return self._twitter_search.get_full_text(*args, **kwargs)

        except RateLimitError:
            if self._update_credentials()
                return self._make_request(*args, **kwargs)
            else return []

        except Exception as error:
            return str(error)

    def _update_credentials(self):
        self._crendential_index += 1
        if self._crendential_index > self._LIMIT_CREDENTIALS:
            return False
        self._twitter_search.auth = os.path.join(self._twitter_search.TWITTER_CREDENTIALS, 
                                                 f'{self._NAME_CREDENTIALS}{self._crendential_index}')
        return True                                          

    @staticmethod
    def _correct_format_fields(flatten_response):
        return {field : (str(value) if isinstance(value, datetime) else value) 
                for field, value in flatten_response.items()}

    @staticmethod
    def _get_day_id(created_at):
        return to_datetime(created_at.date())
