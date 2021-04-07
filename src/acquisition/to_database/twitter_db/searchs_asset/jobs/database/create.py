from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.database \
    import TwitterApiJobsDataBase, TwitterApiStatusDataBase

class CreateTwitterApiJobsDataBase(TwitterApiJobsDataBase):

    @TwitterApiJobsDataBase.try_and_wakeup
    def one(self, *args, **kwargs):
        return self._collection.insert_one(*args, **kwargs)

    @TwitterApiJobsDataBase.try_and_wakeup
    def many(self, *args, **kwargs):
        return self._collection.insert_many(*args, **kwargs)

class CreateTwitterApiStatusDataBase(TwitterApiJobsDataBase):

    @TwitterApiJobsDataBase.try_and_wakeup
    def one(self, *args, **kwargs):
        return self._collection.insert_one(*args, **kwargs)
        
    @TwitterApiJobsDataBase.try_and_wakeup
    def many(self, *args, **kwargs):
        return self._collection.insert_many(*args, **kwargs)