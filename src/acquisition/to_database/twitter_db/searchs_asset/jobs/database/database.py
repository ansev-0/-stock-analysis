from src.database.database import DataBaseAdminCronTab

class TwitterApiJobsDataBase(DataBaseAdminCronTab):

    def __init__(self):
        super().__init__('crontab')
        self._collection = self._database['twitter_searchs_jobs']

    @property
    def collection(self):
        return self._collection

class TwitterApiStatusDataBase(DataBaseAdminCronTab):

    def __init__(self):
        super().__init__('crontab')
        self._collection = self._database['api_status']

    @property
    def collection(self):
        return self._collection
