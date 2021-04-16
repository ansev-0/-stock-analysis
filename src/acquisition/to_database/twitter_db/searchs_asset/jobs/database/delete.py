from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.database \
    import TwitterApiJobsDataBase

class RemoveStatusJob(TwitterApiJobsDataBase):

    @TwitterApiJobsDataBase.try_and_wakeup
    def one(self, *args, **kwargs):
        return self._collection.delete_one(*args, **kwargs)

    def id(self, _id):
        return self.one({'_id' : _id})

    @TwitterApiJobsDataBase.try_and_wakeup
    def many(self, *args, **kwargs):
        return self._collection.delete_many(*args, **kwargs)