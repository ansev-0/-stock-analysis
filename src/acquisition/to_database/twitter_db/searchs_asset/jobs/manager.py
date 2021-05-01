from src.acquisition.to_database.twitter_db.searchs_asset.jobs.rule_trend import RuleTrend
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.find \
    import FindTwitterApiJobsDataBase
from src.acquisition.to_database.twitter_db.searchs_asset.to_database import TwitterSearchToDataBases
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.update import UpdateDateJob
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.update import UpdateTwitterApiStatusDataBase
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.delete import RemoveStatusJob
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.create import CreateNewJob
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.update import UpdateTwitterApiJobsDataBase
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.mutex import MutexSearchsTwitterJob

import os
import pandas as pd
import time
from datetime import datetime

class JobManager:
    _remove_status_job = RemoveStatusJob()
    _update_status_job = UpdateTwitterApiJobsDataBase()
    _create_job = CreateNewJob()
    _rule_trend = RuleTrend()
    _find_api_jobs = FindTwitterApiJobsDataBase()
    _twitter_search_to_db = TwitterSearchToDataBases()
    _update_job = UpdateDateJob()
    _create_job = CreateNewJob()
    _update_status = UpdateTwitterApiStatusDataBase()
    _mutex = MutexSearchsTwitterJob()


    def __init__(self, try_catch_mutex_time='5T', delay_try_mutex=0.2, delay_job='1T', delay_step=0.5):
        
        self._try_catch_mutex_time = pd.to_timedelta(try_catch_mutex_time)
        self.delay_try_mutex = delay_try_mutex
        self.delay_job = pd.to_timedelta(delay_job)
        self.delay_step = delay_step

    def __call__(self, task=None, **kwargs):
        try:
            return self._manage(task=task, **kwargs)

        except Exception as error:
            _id = kwargs['_id']
            folder = 'errors_manager'
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, f'file{_id}.txt'), 'w+') as file:
                file.write(str(error))
            # remove job crontab
            self._update_job.remove_job(_id)
            self._update_status_job.set_error(_id)
            self._remove_status_job.one(_id)
            # mutex
            self._mutex.release()
            #

    @staticmethod
    def _decode_dict_job(task):
        return task['word'], task['_id'], task['since_id'], task['max_id']

    def _get_new_job(self):

        while True:
            jobs = self._get_current_jobs()
            max_delay_created = max(list(map(lambda job: datetime.now() - job['created_at'], jobs)))
            try:
                
                jobs = filter(lambda job: datetime.now() - job['created_at'] > self.delay_job, 
                              jobs)

                jobs = sorted(jobs, key=lambda x: x['created_at'], reverse=True)
                jobs = sorted(jobs, key=lambda x: x['factor_priority'], reverse=True)
                init_job = jobs[0]

            except IndexError:
                time.sleep((self.delay_job - max_delay_created).total_seconds())
            else:
                time.sleep(self.delay_step)
                return self._decode_dict_job(init_job)

    def _manage(self, task=None, **kwargs):

        
        word, _id, since_id, max_id = self._decode_dict_job(task) \
                if task is not None else self._get_new_job()

        while True:
            # set job running
            self._update_status_job.set_running(_id)
            # run job
            dict_status_api, response = self._twitter_search_to_db(word, since_id=since_id, max_id=max_id, **kwargs)
            # notify end job
            self._notify_end_job(_id, isinstance(response, (tuple, list)))
            # manage status
            self._manage_dict_status_api(dict_status_api)
            #try catch mutex
            if not self._try_catch_mutex():
                self._set_mutex_error(_id)
                return None
            # get next jobs by rule
            next_jobs = self._rule_trend(word, since_id, max_id, response)
            # get current_jobs 
            cuurent_jobs = self._get_current_jobs()
            # queue all jobs
            jobs = self._queue_jobs_with_current_jobs(cuurent_jobs + next_jobs)
            # set pending status 
            jobs = self._set_pending_status(jobs)
            # update jobs
            self._push_jobs(jobs)
            # release mutex
            self._mutex.release()
            #get next task
            word, _id, since_id, max_id = self._get_new_job()
            

    

    def _set_mutex_error(self, id_job):
        self._update_status_job.set_mutex_error(id_job)

    def _try_catch_mutex(self):

        date_now = datetime.now()
        while datetime.now() - date_now < self._try_catch_mutex_time:
            if self._mutex.catch():
                return True
            time.sleep(self.delay_try_mutex)
        return False

    def _notify_end_job(self, _id, done):
        if done:
            self._remove_status_job.id(_id)
        else:
            self._update_status_job.set_error(_id)

    def _push_jobs(self, jobs):
        for job in jobs:
            #if '_id' in job[0]:
            if '_id' in job:
                self._update_job.one(job)
                #self._update_job.one(*job)
            else:
                self._create_job.one(job)
                #self._create_job.one(*job)

    def _get_current_jobs(self):
        try:
            return list(self._find_api_jobs.many({'status' : {'$in' : ['pending', 'error']}}))
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
                job['factor_priority'] += (date_now - job['last_update']).total_seconds() / 5
        return jobs

    def _update_jobs(self, jobs):
        for dict_job in jobs:
            self._update_job.one(dict_job)


#manager = JobManager()
#manager(word='bitcoin', _id='prueba')