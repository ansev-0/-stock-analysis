from src.crontab_tasks.crontab_task import TaskCronTab

class CreateRunTaskCronTab(TaskCronTab):

    def add_task(self, module, **kwargs):
        return super().new(command=self._build_path(module), **kwargs)


    def add_daily_task(self, module, **kwargs):
        job = self.add_task(module, **kwargs)
        job.day.every(1)

        return job

cron = CreateRunTaskCronTab()
tasks = ['forex_data_1min_acquisition', 'forex_data_daily_acquisition', 'stock_data_1min_acquisition', 'stock_data_daily_acquisition']
