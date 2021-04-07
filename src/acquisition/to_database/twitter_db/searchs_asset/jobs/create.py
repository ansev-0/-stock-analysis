from src.crontab_tasks.create_task import CreateRunTaskCronTab
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.create import CreateTwitterApiJobsDataBase
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.job import CronTwitterJob
from datetime import datetime

class CreateNewJob(CronTwitterJob):
    
    _cron_tasks = CreateRunTaskCronTab()
    _db_create = CreateTwitterApiJobsDataBase()
    

    def one(self, dict_job, datetime):
        dict_job['_id'] = self._new_id
        # create in db
        self._db_create.one(dict(dict_job, **{'date' : datetime, '_id' : dict_job['_id'], 
                                              'last_update' : datetime.now()}))
        # create cron job
        args_job = self._get_args(dict_job)
        self._cron_tasks.add_datetime_task(f'{self._name_cron_job} {args_job}', datetime)
        # write job
        self._cron_tasks.write()

