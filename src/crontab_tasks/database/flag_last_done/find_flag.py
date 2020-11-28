from src.crontab_tasks.database.flag_last_done.database import FlagsLastDoneCronTab
from datetime import datetime
from pandas import to_timedelta

class FindFlagLastDoneCronTab(FlagsLastDoneCronTab):

    '''
    Wrapper
    '''

    def find_one(self, filter_dict, **kwargs):
        return self.collection.find_one(filter_dict, **kwargs)

    def find_many(self, filter_dict, **kwargs):
        return self.collection.find(filter_dict, **kwargs)

    def find_module(self, module, **kwargs):
        return self.find_one({'_id' : module}, **kwargs)

    def find_modules(self, modules, **kwargs):
        return self.find({'_id' : {'$in' : modules}}, **kwargs)

    def find_modules_need_exec(self, modules=None):
        filter_dict = modules if modules is not None else  {}
        return [module['_id'] for module in self.find_many(filter_dict) 
                if self._need_exec(module)]

    def _need_exec(self, module):
        return to_timedelta(module['time_to_next_flag']) + module['last_time'] < datetime.now()
