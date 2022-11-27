from time import time
from datetime import datetime

class Listener:
    
    def __init__(self, find_jobs, delay=1):
        self.delay = 1
        self._find_jobs = find_jobs

    @property
    def find_jobs(self):
        return self._find_jobs

    def __call__(self, status=None):
        jobs = []
        while len(jobs) == 0:
            jobs = list(self.find_jobs.many({'status' : self._status_decoded(status), 
                                             'date' : {'$lt' : datetime.now()}}))
            time.sleep(self.delay)
        return jobs

    @staticmethod
    def _status_decoded(status):
        if isinstance(status, str):
            return status
        elif isinstance(status, (tuple, list)):
            return {'$in' : list(status)}
        elif status is None:
            return 'pending'
        raise ValueError('Invalid status parameter')