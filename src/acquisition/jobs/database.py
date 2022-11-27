from src.database.database import DataBaseJobsAcquisition

class DataBaseJobs(DataBaseJobsAcquisition):
    COLLECTION_NAME = 'acquisition_jobs'
    def __init__(self):
        super().__init__('crontab')
        self._collection = self._database[self.COLLECTION_NAME]
        
class FindJobsDB(DataBaseJobs):

    def one(self, *args, **kwargs):
        return self._collection.find_one(*args, **kwargs)

    def many(self, *args, **kwargs):
        return self._collection.find(*args, **kwargs)

    def id(self, id):
        return self.one({'_id' : id})

class UpdateJobsDB(DataBaseJobs):
    def one(self, *args, **kwargs):
        return self._collection.update_one(*args, **kwargs)

    def many(self, *args, **kwargs):
        return self._collection.update_many(*args, **kwargs)

    def id(self, id, dict_to_update, **kwargs):
        return self.one({'_id' : id}, dict_to_update, **kwargs)

class UpdateStatusJobsDB(UpdateJobsDB):

    def running(self, id):
        return self.id(id, {'$set' : self._default_dict_status('running')})

    def error(self, id, error):
        return self.id(id, 
            {'$set' : dict(self._default_dict_status('error'), 
                          **{'error' : str(error)})
            }
        )
    def done(self, id):
        return self.id(id, {'$set' : self._default_dict_status('done')})
