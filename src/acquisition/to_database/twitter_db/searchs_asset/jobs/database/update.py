from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.database import TwitterApiJobsDataBase, TwitterApiStatusDataBase
from datetime import datetime

class UpdateTwitterApiJobsDataBase(TwitterApiJobsDataBase):

    @TwitterApiJobsDataBase.try_and_wakeup
    def one(self, where, dict_to_update, **kwargs):
        return self._collection.update_one(where, self._set_update(dict_to_update), **kwargs)

    @TwitterApiJobsDataBase.try_and_wakeup
    def many(self, where, dict_to_update, **kwargs):
        return self._collection.update_many(where, self._set_update(dict_to_update), **kwargs)

    def set_mutex_error(self, id_job):
        return self.one({'_id' : id_job}, {'status' : 'mutex error'})

    def set_running(self, id_job):
        return self.one({'_id' : id_job}, {'status' : 'running'})

    
    def set_error(self, id_job):
        return self.one({'_id' : id_job}, {'status' : 'error'})

    
    def set_done(self, id_job):
        return self.one({'_id' : id_job}, {'status' : 'done'})

    
    def _set_update(self, dict_to_update):
        return {'$set' : dict_to_update}

class UpdateTwitterApiStatusDataBase(TwitterApiStatusDataBase):

    @TwitterApiStatusDataBase.try_and_wakeup
    def one(self, where, dict_to_update, **kwargs):
        return self._collection.update_one(where, self._set_update(dict_to_update), **kwargs)

    @TwitterApiStatusDataBase.try_and_wakeup
    def many(self, where, dict_to_update, **kwargs):
        return self._collection.update_many(where, self._set_update(dict_to_update), **kwargs)

    @TwitterApiStatusDataBase.try_and_wakeup
    def set_unavailable(self, api_user, error):
        return self._collection.update_one({'api_user' : api_user}, 
                                           self._set_update({'available' : False, 
                                                             'error' : error, 
                                                             'last_update_by_job' : datetime.now()}),
                                            **kwargs)

    def set_available(self, api_user, error):
        return self.one({'api_user' : api_user}, 
                        {'available' : True, 
                         'error' : None, 
                         'last_update_by_job' : datetime.now()},
                        **kwargs)

    @TwitterApiStatusDataBase.try_and_wakeup    
    def incr_request(self, api_user):
        return self._collection.update_one({'api_user' : api_user}, self._incr_dict)


    @TwitterApiStatusDataBase.try_and_wakeup
    def incr_requests(self, api_users):
        return self._collection.update_many({'api_user' : {'$in' : api_users}}, self._incr_dict)

       
    def reset_request(self, api_user):
        self.one({'api_user' : api_user}, self._reset_dict)

    
    def reset_requests(self, api_users):
        self.many({'api_user' : {'$in' : api_users}}, self._reset_dict)

    @property
    def _incr_dict(self):
        return {'$inc' : {'requests' : 1, 'remaining' : -1}, 
                **self._set_update({'waiting' : False, 
                                    'available' : True,
                                    'last_update_by_job' : datetime.now(),
                                    'error' : None})}

    @property
    def _reset_dict(self):
        return {'remaining' : 0,
                'waiting' : True,
                'error' : None,
                'last_update_by_job' : datetime.now(),
                'available' : True}

    def _set_update(self, dict_to_update):
        return {'$set' : dict_to_update}
