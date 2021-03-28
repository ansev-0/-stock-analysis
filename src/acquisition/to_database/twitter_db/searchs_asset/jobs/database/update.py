from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.database import TwitterApiJobsDataBase, TwitterApiStatusDataBase
from datetime import datetime

class UpdateTwitterApiJobsDataBase(TwitterApiJobsDataBase):

    def one(self, where, dict_to_update, **kwargs):
        return self._collection.update_one(where, self._set_update(dict_to_update), **kwargs)

    def many(self, where, dict_to_update, **kwargs):
        return self._collection.update_many(where, self._set_update(dict_to_update), **kwargs)

    def _set_update(self, dict_to_update):
        return {'$set' : dict_to_update}

class UpdateTwitterApiStatusDataBase(TwitterApiStatusDataBase):

    def one(self, where, dict_to_update, **kwargs):
        return self._collection.update_one(where, self._set_update(dict_to_update), **kwargs)

    def many(self, where, dict_to_update, **kwargs):
        return self._collection.update_many(where, self._set_update(dict_to_update), **kwargs)

    def set_unavailable(self, api_user, error):
        return self._collection.update_one({'api_user' : api_user}, 
                                           self._set_update({'available' : False, 'error' : error}),
                                            **kwargs)
        
    def incr_request(self, api_user):
        return self._collection.update_one({'api_user' : api_user}, self._incr_dict)



    def incr_requests(self, api_users):
        return self._collection.update_many({'api_user' : {'$in' : api_users}}, self._incr_dict)
        
    def reset_request(self, api_user):
        self._collection.update_one({'api_user' : api_user}, 
                                    self._reset_dict)

    def reset_request(self, api_users):
        self._collection.update_many({'api_user' : {'$in' : api_users}}, 
                                     self._reset_dict)

    @property
    def _incr_dict(self):
        return {'$incr' : {'requests' : 1, 'remaining' : -1}}

    @property
    def _reset_dict(self):
        return self._set_update({'requests' : 0, 
                                 'remaining' : 0,
                                 'reset_date' : datetime.now(), 
                                 'waiting' : True})

    def _set_update(self, dict_to_update):
        return {'$set' : dict_to_update}

