from src.crontab_tasks.database.flag_last_done.find_flag import FindFlagLastDoneCronTab
from src.crontab_tasks.database.flag_last_done.update_flag import UpdateFlagLastTimeDoneCrontab
from src.crontab_tasks.database.flag_last_done.create_flag import CreateFlagLastDoneCronTab
from src.crontab_tasks.database.flag_last_done.find_and_update import FindAndUpdateErrorsCronTab
from datetime import datetime

class TaskManager:

    _find_flags = FindFlagLastDoneCronTab()
    _update_flags = UpdateFlagLastTimeDoneCrontab()
    _create_flags = CreateFlagLastDoneCronTab()
    _find_and_update_errors_flags = FindAndUpdateErrorsCronTab()

    def __init__(self, attemps=1):
        self._errors = None
        self.attemps = attemps
        
    @property
    def errors(self):
        return self._errors

    def __call__(self, name_module, task):

        if self._need_exec(name_module):
            self._run_task(task, name_module)


    def _run_task(self, task, name_module):

        for attemp in range(self.attemps):
            try:
                task()
            except Exception as error:
                #add error from attemp
                self._errors.append({'time_error' : datetime.now(), 'message' : error})

            else:
                #if not errors update last time dome
                self._update_errors(name_module) 
                return self._update_flags.update_flag(name_module)
        else:
            self._update_errors(name_module)

    def _update_errors(self, name_module):
        #update errors for task in db
        if self._errors is not None:
            self._find_and_update_errors_flags(name_module, self._errors)
            self._errors = None


    def _need_exec(self, module):
        try:
            #if task exist check if exec is needed
            return self._find_flags.module_need_exec(module)

        except TypeError:
            # if task not exist create it an run
            self._create_flags.create_one(module)
            return True
             
        
        
