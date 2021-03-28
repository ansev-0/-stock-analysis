from src.acquisition.to_database.twitter_db.searchs_asset.jobs.rule_trend import RuleTrend
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.database.find \
    import FindTwitterApiJobsDataBase, FindTwitterApiStatusDataBase
from src.acquisition.to_database.twitter_db.searchs_asset.to_database import TwitterSearchToDataBases
from src.acquisition.to_database.twitter_db.searchs_asset.jobs.update import UpdateDateJob
from src.acquisition.to_database.twitter_db.searchs_asset.job.database.update import UpdateTwitterApiStatusDataBase
import os

class JobManager:

    _rule_trend = RuleTrend()
    _find_api_jobs = FindTwitterApiJobsDataBase()
    _find_api_status = FindTwitterApiStatusDataBase()
    _twitter_search_to_db = TwitterSearchToDataBases()
    _update_job = UpdateDateJob()
    _update_status = UpdateTwitterApiStatusDataBase()

    def __init__(self, time_step):
        self.time_step = time_step
    
    def __call__(self, word, *args, **kwargs):

        # run job
        dict_status, response = self._twitter_search_to_db(word, *args, **kwargs)
        # manage status
        self._manage_dict_status(dict_status)
        # get others jobs
        current_jobs = self._get_current_jobs
        # get next jobs by rule
        next_jobs = self._rule_trend(word, response) if isinstance(response, list) and len(response) > 0 else []
        # get jobs
        jobs = self._sort_jobs(current_jobs, next_jobs)
        # update jobs
        self._update_job(jobs)

    def _manage_dict_status(self, dict_status):

        for user, status in dict_status.items():
            if isinstance(user, str):
                self._update_status.set_unavailable(user, status) 
            elif status:
                self._update_status.incr_request(user)
            elif not status:
                self._update_status.reset_request(user)


    def _update_jobs(self, jobs):
        for dict_job, datetime in jobs:
            self._update_job.one(dict_job, datetime)

    @property
    def _current_jobs(self):
        try:
            return list(self._find_api_jobs.many({}))
        except Exception:
            return []





