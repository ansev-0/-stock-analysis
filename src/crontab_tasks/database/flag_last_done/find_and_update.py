from src.crontab_tasks.database.flag_last_done.update_flag import UpdateFlagErrorsCrontab
from src.crontab_tasks.database.flag_last_done.find_flag import FindFlagLastDoneCronTab

class FindAndUpdateErrorsCronTab(UpdateFlagErrorsCrontab, FindFlagLastDoneCronTab):

    def __call__(self, task_id, errors, **kwargs):
        
        try:
            current_errors = self.find_module(task_id)['errors']
        except KeyError:
            current_errors = []
        
        return self.update_errors(task_id, errors + current_errors, **kwargs)
