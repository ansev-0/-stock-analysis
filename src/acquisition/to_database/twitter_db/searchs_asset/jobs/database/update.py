from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.database import TwitterApiJobsDataBase, TwitterApiStatusDataBase
from datetime import datetime

class UpdateTwitterApiJobsDataBase(TwitterApiJobsDataBase):

    def one(self, where, *args, **kwargs):
        return self._collection.update_one(self._set_update(where) *args, **kwargs)

    def many(self, where, *args, **kwargs):
        return self._collection.update_many(self._set_update(where) *args, **kwargs)

    def _set_update(self, dict_to_update):
        return {'$set' : dict_to_update}

class UpdateTwitterApiStatusDataBase(TwitterApiStatusDataBase):

    def one(self, where, *args, **kwargs):
        return self._collection.update_one(self._set_update(where) *args, **kwargs)

    def many(self, where, *args, **kwargs):
        return self._collection.update_many(self._set_update(where) *args, **kwargs)
        
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
        return {'$incr' : {'requests' : 1}}

    @property
    def _reset_dict(self):
        return self._set_update({'requests' : 0, 
                                 'reset_date' : datetime.now()})

    def _set_update(self, dict_to_update):
        return {'$set' : dict_to_update}

