from src.crontab_tasks.crontab_task import TaskCronTab
from datetime import datetime 

class CreateRunTaskCronTab(TaskCronTab):

    _DATETIME_ATTR = ('month', 'day', 'hour', 'minute')

    def add_task(self, module, prefix=None, **kwargs):
        path = self._build_path(module)
        prefix = prefix if prefix is not None else ''
        return super().new(command=f'{prefix}{path}', **kwargs)

    def add_monthly_task(self, module, **kwargs):
        job = self.add_task(module, **kwargs)
        job.every(1).month()
        return job

    def add_daily_task(self, module, **kwargs):
        job = self.add_task(module, **kwargs)
        job.every(1).days()
        return job

    def add_reboot_task(self, module, **kwargs):
        job = self.add_task(module, prefix="sleep 90 & ", **kwargs)
        job.every_reboot()
        return job

    def add_datetime_task(self, module, date, **kwargs):
        self._check_datetime(date)
        job = self.add_task(module, **kwargs)
        for attr in self._DATETIME_ATTR:
            getattr(job, attr).on(getattr(date, attr))
        return job

    @staticmethod
    def _check_datetime(date):
        if not isinstance(date, datetime):
            raise TypeError('You must pass a instance of datetime.datetime')
