from src.crontab.crontab import TaskCronTab

class CreateRunTaskCronTab(TaskCronTab):

    def add_task(self, module, frecuency, **kwargs):
        return super().new(command=self._build_path(module), **kwargs)


    def add_daily_task(self, module, **kwargs):
        job = self.add_task(module, **kwargs)
        job.day.every(1)

        return job


