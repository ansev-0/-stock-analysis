from crontab import CronTab
import os
from datetime import datetime
from src.tools.path import get_financial_path

class TaskCronTab(CronTab):

    _task_folder = os.path.join(get_financial_path(), 'src/crontab_tasks/tasks')

    def __init__(self, user=True, **kwargs):
        super().__init__(user=user, **kwargs)

    def _build_path(self, module):
        path = os.path.join(self._task_folder, module)
        return f'python3 {path}'




#cron = TaskCronTab()
#print(cron.intab)
#for job in cron:
#    
#    print(job)
#    print(job.is_enabled())
#    #print(job.is_valid())
#    print(job.schedule(date_from=datetime.now()).get_next())
#    if '_id' in job.command:
#        cron.remove(job)
#    #print(type(job.schedule(date_from=datetime.now()).get_next()))
#    #cron.remove(job)
#cron.write()





