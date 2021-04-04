from src.crontab_tasks.database.flag_last_done.find_flag import FindFlagLastDoneCronTab
from src.crontab_tasks.database.flag_last_done.update_flag import UpdateFlagLastTimeDoneCrontab
from src.crontab_tasks.database.flag_last_done.create_flag import CreateFlagLastDoneCronTab
from src.crontab_tasks.database.flag_last_done.find_and_update import FindAndUpdateErrorsCronTab
from src.tools.mongodb import restart_connect_mongodb
from datetime import datetime
import json
import os
import time
from src.tools.path import get_financial_path
from src.exceptions.to_database_exceptions import ToDataBaseError
from pymongo.errors import ServerSelectionTimeoutError


class TaskManager:

    _find_flags = FindFlagLastDoneCronTab()
    _update_flags = UpdateFlagLastTimeDoneCrontab()
    _find_and_update_errors_flags = FindAndUpdateErrorsCronTab()

    def __init__(self, attemps=1, time_sleep=10, freq=None, attempt_connection_refused=4):

        self._errors = []
        self.attemps = attemps
        self.time_sleep = time_sleep
        self._create_flags = CreateFlagLastDoneCronTab(freq)
        self.attempt_connection_refused = attempt_connection_refused
        
    @property
    def errors(self):
        return self._errors

    def __call__(self, name_module, task):
        self._try_connect_and_run(name_module, task, 0)

    def _try_connect_and_run(self, name_module, task, number_of_try):
        
        try:
            if self._need_exec(name_module):
                self._run_task(task, name_module)

        except ServerSelectionTimeoutError as error:
            
            if number_of_try <= self.attempt_connection_refused:
                restart_connect_mongodb()
                self._try_connect_and_run(name_module, task, number_of_try + 1)


    def _run_task(self, task, name_module):

        for attemp in range(self.attemps):
            try:
                task()
            except Exception as error:
                #add error from attemp
                self._errors.append({'time_error' : datetime.now(), 'message' : str(error)})

            except ToDataBaseError as error:
                self._errors.append({'time_error' : datetime.now(), 'message' : str(error)})
            
            except ServerSelectionTimeoutError as error:
                try:
                    restart_connect_mongodb()
                    task()

                except Exception as error:
                    self._errors.append({'time_error' : datetime.now(), 'message' : str(error)})

                else:
                    #if not errors update last time done
                    self._update_errors(name_module)
                    return self._update_flags.update_flag(name_module)
            else:
                #if not errors update last time done
                self._update_errors(name_module) 
                return self._update_flags.update_flag(name_module)
            
            time.sleep(self.time_sleep)
        else:
            self._update_errors(name_module)

    def _update_errors(self, name_module):
        self._find_and_update_errors_flags(name_module, self._errors)
        self._errors = []


    def _need_exec(self, module):
        try:
            #if task exist check if exec is needed
            return self._find_flags.module_need_exec(module)

        except TypeError:
            # if task not exist create it an run
            self._create_flags.create_one(module)
            return True
