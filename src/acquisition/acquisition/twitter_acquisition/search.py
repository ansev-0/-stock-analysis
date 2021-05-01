from src.acquisition.acquisition.twitter_acquisition.twitter_request import TwitterAPIAuthJson
from tweepy import Cursor

class TwitterSearchPopular(TwitterAPIAuthJson):

    _DEFAULT_KEYS = {'result_type' : 'popular'}

    def get(self, q, **kwargs):
        return self._get_with_default_keys(default_keys=None, q=q, **kwargs)

    def get_full_text(self, q, **kwargs):
        return self._get_with_default_keys({'tweet_mode' : 'extended'}, q=q,
                                             **kwargs)


    def _get_with_default_keys(self, default_keys, **kwargs):

        default_keys = dict(self._DEFAULT_KEYS, **default_keys.copy()) \
            if default_keys is not None else self._DEFAULT_KEYS
        dict_kwargs = dict({key : value 
                            for key, value in kwargs.items() 
                            if key not in default_keys}, 
                            **default_keys)
        try:
            return [status for status in Cursor(self.search, **dict_kwargs).items(1000)]
        except Exception:
            return self.search(**dict_kwargs)
        
