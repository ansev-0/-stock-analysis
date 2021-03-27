class CronTwitterJob:
    
    _name_cron_job = 'twitter_search_job.py'

    @staticmethod
    def _get_args(self, dict_job):
        id1 = dict_job['id1']
        id2 = dict_job['id2']
        word = dict_job['word']
        return f'--word {word} --id1 {id1} --id2{id2}'
