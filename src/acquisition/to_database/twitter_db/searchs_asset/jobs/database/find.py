from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.database\
     import TwitterApiJobsDataBase, TwitterApiStatusDataBase

class FindTwitterApiJobsDataBase(TwitterApiJobsDataBase):

    @TwitterApiJobsDataBase.try_and_wakeup
    def one(self, *args, **kwargs):
        return self._collection.find_one(*args, **kwargs)

    @TwitterApiJobsDataBase.try_and_wakeup
    def many(self, *args, **kwargs):
        return self._collection.find(*args, **kwargs)

    def word(self, word, **kwargs):
        return self.many({'word' : (word if isinstance(word, str) 
                                    else {'$in' : word})}, **kwargs)

    def before_date(self, before_date, **kwargs):
        return self.many({'created_at_end' : {'$lt' : before_date}}, **kwargs)

    def after_date(self, after_date, **kwargs):
        return self.many({'created_at_end' : {'$gt' : after_date}}, **kwargs)

    def before_id(self, before_id, **kwargs):
        return self.many({'created_at_end' : {'$lt' : before_id}}, **kwargs)

    def after_id(self, after_id, **kwargs):
        return self.many({'created_at_end' : {'$gt' : after_id}}, **kwargs)

    def between_dates(self, init_date, end_date, **kwargs):
        return self.many({'created_at_end' : {'$lt' : end_date, '$gt' : init_date}}, **kwargs)

    def between_ids(self, init_id, end_id, **kwargs):
        return self.many({'created_at_end' : {'$lt' : end_id, '$gt' : init_id}}, **kwargs)

class FindTwitterApiStatusDataBase(TwitterApiStatusDataBase):

    @TwitterApiStatusDataBase.try_and_wakeup
    def one(self, api_user, **kwargs):
        return self._collection.find_one({'api_user' : api_user}, 
                                         **kwargs)
    @TwitterApiStatusDataBase.try_and_wakeup
    def many(self, api_users, **kwargs):
        return self._collection.find({'api_user' : {'$in' : api_users}}, 
                                     **kwargs)
