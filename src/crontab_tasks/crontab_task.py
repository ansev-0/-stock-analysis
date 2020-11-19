from crontab import CronTab
import os

class TaskCronTab(CronTab):

    _task_folder = 'home/antonio/financialworks/src/crontab_tasks/tasks'

    def __init__(self, user=True, **kwargs):
        super().__init__(user=user, **kwargs)

    def _build_path(self, module):
        path = os.path.join(self._task_folder, module)
        return f'python3 {path}'




