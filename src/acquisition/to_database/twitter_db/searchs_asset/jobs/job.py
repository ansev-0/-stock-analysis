class CronTwitterJob:
    
    _name_cron_job = 'twitter_search_job.py'

    @staticmethod
    def _get_args(self, dict_job):
        return ' --_id {_id} --word {word} --id1 {id1} --id2{id2}'\
            .format(dict_job['_id'], dict_job['word'], dict_job['id1'], dict_job['id2'])

    @property
    def _new_id(self):
        return int(datetime.now().timestamp() *  10e5)