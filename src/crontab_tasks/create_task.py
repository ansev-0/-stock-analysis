from src.crontab_tasks.crontab_task import TaskCronTab
from datetime import datetime 

class CreateRunTaskCronTab(TaskCronTab):

    def add_task(self, module, **kwargs):
        return super().new(command=self._build_path(module), **kwargs)

    def add_daily_task(self, module, **kwargs):
        job = self.add_task(module, **kwargs)
        job.every(1).days()
        return job

    def add_reboot_task(self, module, **kwargs):
        job = self.add_task(module, **kwargs)
        job.every_reboot()
        return job
