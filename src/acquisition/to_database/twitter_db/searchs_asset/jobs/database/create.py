from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.database \
    import TwitterApiJobsDataBase, TwitterApiStatusDataBase

class CreateTwitterApiJobsDataBase(TwitterApiJobsDataBase):

    def one(self, *args, **kwargs):
        return self._collection.create_one(*args, **kwargs)

    def many(self, *args, **kwargs):
        return self._collection.create_many(*args, **kwargs)

class CreateTwitterApiStatusDataBase(TwitterApiJobsDataBase):

    def one(self, *args, **kwargs):
        return self._collection.create_one(*args, **kwargs)

    def many(self, *args, **kwargs):
        return self._collection.create_many(*args, **kwargs)