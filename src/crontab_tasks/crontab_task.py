from crontab import CronTab
import os
from datetime import datetime

class TaskCronTab(CronTab):

    _task_folder = 'src/crontab_tasks/tasks'

    def __init__(self, user=True, **kwargs):
        super().__init__(user=user, **kwargs)

    def _build_path(self, module):
        path = os.path.join(self._task_folder, module)
        return f'python3 {path}'


cron = TaskCronTab()
for job in cron:
    
    print(job)
    print(job.is_enabled())
    print(job.is_valid())
    print(job.schedule(date_from=datetime.now()).get_next())




