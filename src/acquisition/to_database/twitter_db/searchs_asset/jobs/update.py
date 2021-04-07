from src.crontab_tasks.create_task import CreateRunTaskCronTab
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.update import UpdateTwitterApiJobsDataBase
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.job import CronTwitterJob
from datetime import datetime

class UpdateDateJob(CronTwitterJob):

    _cron_tasks = CreateRunTaskCronTab()
    _db_update = UpdateTwitterApiJobsDataBase()
    
    def one(self, dict_job, datetime):
        self._update_cron(dict_job, datetime)
        self._update_in_db(dict_job, datetime)


    def _update_cron(self, dict_job, date_job):
        # add new job
        args_job = self._get_args(dict_job)
        
        self._cron_tasks.add_datetime_task(f'{self._name_cron_job} {args_job}' , date_job)
        # remove old
        self.remove_job(dict_job['_id'])

    def remove_job(self, _id):
        for job in self._cron_tasks:
            if str(_id) in job.command:
                self._cron_tasks.remove(job)

    def _update_in_db(self, dict_job, date_job):
        # build dict to replace
        dict_to_replace = dict_job.copy()
        # replace date
        dict_to_replace['date'] = date_job
        #update last update
        dict_to_replace['last_update'] = datetime.now()
        # update database
        self._db_update.one({'_id' : dict_job['_id']}, 
                            dict_to_replace, 
                            upsert=True)

    