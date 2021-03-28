from src.crontab_tasks.create_task import CreateRunTaskCronTab
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.update import UpdateTwitterApiJobsDataBase
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.job import CronTwitterJob

class UpdateDateJob(CronTwitterJob):

    _update_keys = ('date', 'word', 'id1', 'id2')
    _cron_tasks = CreateRunTaskCronTab()
    _db_update = UpdateTwitterApiJobsDataBase()
    
    def one(self, dict_job, datetime):
        self._update_cron(dict_job, datetime)
        self._update_in_db(dict_job, datetime)


    def _update_cron(self, dict_job, datetime):
        for job in self._cron_tasks:
            job.schedule(date_from=datetime.now()).get_next()
            if self.is_this_job(dict_job, job):
                # add new job
                self._cron_tasks.add_datetime_task(job.command, datetime)
                # remove
                self._cron_tasks.remove(job)


    def _update_in_db(self, dict_job, datetime):
        # build dict to replace
        dict_to_replace = dict_job.copy()
        dict_to_replace['date'] = datetime
        # update database
        self._db_update({key : dict_job[key] 
                         for key in self._update_keys}, dict_to_replace)

    @staticmethod
    def is_this_job(dict_job, job):
        command = job.command
        return job.schedule(date_from=datetime.now()).get_next() == dict_job['date']\
            and all(dict_job[key] in command for key in self._update_keys[1:])