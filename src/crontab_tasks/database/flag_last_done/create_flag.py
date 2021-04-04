from pandas import to_timedelta
from datetime import datetime
from src.crontab_tasks.database.flag_last_done.insert_flag import InsertFlagLastDoneCronTab
from src.tools.reduce_tools import combine_dicts


class CreateFlagLastDoneCronTab(InsertFlagLastDoneCronTab):

    def __init__(self, time_to_next_flag=None):
        super().__init__()
        self.time_to_next_flag = time_to_next_flag

    #public properties
    @property
    def time_to_next_flag(self):
        return self._time_to_next_flag

    @time_to_next_flag.setter
    def time_to_next_flag(self, time_to_next_flag):
        self._time_to_next_flag = time_to_next_flag \
            if time_to_next_flag is not None else str(to_timedelta('0 days 23:00:00'))

    #private properties
    @property
    def _default_dict_params(self):
        return {'last_time' : datetime.now(), 'time_to_next_flag' : self._time_to_next_flag}

    #public methods of instance
    def create_one(self, module, **kwargs):
        return self.insert_one(self._get_dict_to_insert(module), 
                               **kwargs)

    def create_many(self, list_module, **kwargs):
        return self.insert_many([self._get_dict_to_insert(module) 
                                 for module in list_module], 
                                **kwargs)

    #private methods of instance
    def _get_dict_to_insert(self, module):
        return combine_dicts(self._default_dict_params, {'_id' : module})
