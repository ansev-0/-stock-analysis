from src.database.database import DataBaseAdminCronTab

class MutexSearchsTwitterJob(DataBaseAdminCronTab):

    ID = 'mutex'

    def __init__(self):
        super().__init__('crontab')
        self._collection = self._database['twitter_searchs_mutex']

    @property
    def collection(self):
        return self._collection

    def catch(self):
        if not self.status():
            self._update_status(True)
            return True
        return False

    @DataBaseAdminCronTab.try_and_wakeup
    def status(self):
        try:
            return self._collection.find_one({'_id' : self.ID}, 
                                          projection={'status' : True, '_id' : False})['status']
        except Exception as error:
            return False

    def release(self):
        return self._update_status(False)

    @DataBaseAdminCronTab.try_and_wakeup
    def _update_status(self, status):
        return self._collection.update_one({'_id' : self.ID}, {'$set' : {'status' : status}}, upsert=True)


