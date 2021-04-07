from datetime import datetime

class CronTwitterJob:
    
    _name_cron_job = 'twitter_search_job.py'

    @staticmethod
    def _get_args(dict_job):
        return ' '.join([f'--{key} {dict_job[key]}' for key in ('_id', 'word', 'since_id', 'max_id')])

    @property
    def _new_id(self):
        return int(datetime.now().timestamp() *  10e5)