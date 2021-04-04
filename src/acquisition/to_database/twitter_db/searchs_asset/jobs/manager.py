from src.acquisition.to_database.twitter_db.searchs_asset.jobs.rule_trend import RuleTrend
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.find \
    import FindTwitterApiJobsDataBase, FindTwitterApiStatusDataBase
from src.acquisition.to_database.twitter_db.searchs_asset.to_database import TwitterSearchToDataBases
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.update import UpdateDateJob
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.update import UpdateTwitterApiStatusDataBase
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.create import CreateNewJob
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.update import UpdateTwitterApiJobsDataBase
import os
import pandas as pd

class JobManager:
    
    _update_status_job = UpdateTwitterApiJobsDataBase()
    _create_job = CreateNewJob()
    _rule_trend = RuleTrend()
    _find_api_jobs = FindTwitterApiJobsDataBase()
    _find_api_status = FindTwitterApiStatusDataBase()
    _twitter_search_to_db = TwitterSearchToDataBases()
    _update_job = UpdateDateJob()
    _create_job = CreateNewJob()
    _update_status = UpdateTwitterApiStatusDataBase()

    def __init__(self, time_step='530MS', delay_start_job = '5T'):
        self.time_step = pd.to_timedelta(time_step)
        self._delay_start_job = pd.to_timedelta(delay_start_job)

    @property
    def date_starts_job(self):
        return datetime.now() + self._delay_start_job
    
    def __call__(self, word, _id, *args, **kwargs):
        # set job running
        self._update_status_job.set_running(_id)
        # run job
        dict_status_api, response = self._twitter_search_to_db(word, *args, **kwargs)
        # notify end job
        self._notify_end_job(_id, isinstance(response, (tuple, list)))
        # manage status
        self._manage_dict_status_api(dict_status_api)
        # get next jobs by rule
        next_jobs = self._rule_trend(word, response)
        # get current_jobs 
        cuurent_jobs = self._get_current_jobs()
        # queue all jobs
        jobs = self._queue_jobs_with_current_jobs(cuurent_jobs + next_jobs)
        # set pending status 
        jobs = self._set_pending_status(jobs)
        # date starts jobs
        date_starts_jobs = self.date_starts_job
        # assign dates
        jobs = self._assign_dates(jobs, date_starts_jobs)
        # update jobs
        self._push_jobs(jobs)

    def _notify_end_job(self, _id, done):
        if done:
            self._update_status_job.set_done(_id)
        else:
            self._update_status_job.set_error(_id)

    def _push_jobs(self, jobs):
        for job in jobs:
            if '_id' in job:
                self._update_job.one(*job)
            else:
                self._create_job.one(*job)

    def _assign_dates(self, jobs, date_start):
        return [(job, date_start + (self.time_step * i)) for i, job in enumerate(jobs)]

    def _get_current_jobs(self, date_start_jobs):
        try:
            return list(self._find_api_jobs.many({'status' : 'pending', 
                                                  'date': {'$gt' : date_starts_jobs}}))
        except Exception as error:
            return []

    def _queue_jobs_with_current_jobs(self, jobs):
        # update factor priority 
        jobs = self._update_factor_priority(jobs)
        # get correct order
        jobs = sorted(jobs, 
                      key=lambda dict_job: dict_job['factor_priority'], 
                      reverse=True)
        return jobs

    @staticmethod
    def _set_pending_status(jobs):
        for job in jobs:
            job['status'] = 'pending'
        return jobs
        
    def _manage_dict_status_api(self, dict_status):

        for user, status in dict_status.items():
            if isinstance(status, str):
                self._update_status.set_unavailable(user, status) 
            elif status:
                self._update_status.incr_request(user)
            elif not status:
                self._update_status.reset_request(user)

    def _update_factor_priority(self, jobs):
        date_now = datetime.now()
        for job in jobs:
            if 'last_update' in job:
                job['factor_priority'] += (job['last_update'] - date_now).total_seconds()
        return jobs

    def _update_jobs(self, jobs):
        for dict_job, datetime in jobs:
            self._update_job.one(dict_job, datetime)


manager = JobManager()
manager(word='bitcoin', _id='prueba')