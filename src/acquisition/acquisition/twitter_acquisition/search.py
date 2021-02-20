from src.acquisition.acquisition.twitter_acquisition.twitter_request import TwitterAPIAuthJson

class TwitterSearchPopular(TwitterAPIAuthJson):
    def get(self, *args, **kwargs):
        return self.search(*args, **{key : value 
                                     for key, value in kwargs.items() 
                                     if key != 'result_type'}, 
                           result_type='popular')
