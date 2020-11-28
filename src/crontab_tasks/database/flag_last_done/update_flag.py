from src.crontab_tasks.database.flag_last_done.database import FlagsLastDoneCronTab
from datetime import datetime

class UpdateFlagLastDoneCronTab(FlagsLastDoneCronTab):

    '''
    Wrapper
    '''

    def update_one(self, where, values, **kwargs):
        return self.collection.update_one(where, self._dict_set(values), **kwargs)

    def update_many(self, where, values, **kwargs):
        return self.collection.update_many(where, self._dict_set(values), **kwargs)

    @staticmethod
    def _dict_set(values):
        return {'$set' : values}


class UpdateFlagLastTimeDoneCrontab(UpdateFlagLastDoneCronTab):

    def update_flag(self, task_id, **kwargs):
        return self.update_one({'_id' : task_id}, {'last_time' : datetime.now()}, **kwargs)

    def update_many_flags(self, task_ids):
        return self.update_many({'_id' : {'$in' : task_ids}}, {'last_time' : datetime.now()})


class UpdateFlagMinTimeToNextDoneCrontab(UpdateFlagLastDoneCronTab):

    def update_min_time(self, task_id, time, **kwargs):
        return self.update_one({'_id' : task_id}, {'time_to_next_flag' : time}, **kwargs)

    def update_many_min_times(self, task_ids, time):
        return self.update_many({'_id' : {'$in' : task_ids}}, {'time_to_next_flag' : time})
