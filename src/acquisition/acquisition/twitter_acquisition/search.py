from src.acquisition.acquisition.twitter_acquisition.twitter_request import TwitterAPIAuthJson

class TwitterSearchPopular(TwitterAPIAuthJson):

    _DEFAULT_KEYS = {'result_type' : 'popular'}

    def get(self, *args, **kwargs):
        return self._get_with_default_keys(default_keys=None, *args, **kwargs)

    def get_full_text(self, *args, **kwargs):
        return self._get_with_default_keys({'tweet_mode' : 'extended'}, 
                                            *args, **kwargs)


    def _get_with_default_keys(self, default_keys, *args, **kwargs):

        default_keys = dict(self._DEFAULT_KEYS, **default_keys.copy()) \
            if default_keys is not None else self._DEFAULT_KEYS

        return self.search(*args, **{key : value 
                                     for key, value in kwargs.items() 
                                     if key not in default_keys}, 
                           **default_keys)
                           