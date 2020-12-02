from src.crontab_tasks.crontab_task import TaskCronTab
from datetime import datetime 

class CreateRunTaskCronTab(TaskCronTab):

    def add_task(self, module, prefix=None, **kwargs):
        path = self._build_path(module)
        prefix = prefix if prefix is not None else ''
        return super().new(command=f'{prefix}{path}', **kwargs)

    def add_daily_task(self, module, **kwargs):
        job = self.add_task(module, **kwargs)
        job.every(1).days()
        return job

    def add_reboot_task(self, module, **kwargs):
        job = self.add_task(module, prefix="sleep 100 && ", **kwargs)
        job.every_reboot()
        return job


