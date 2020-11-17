from src.crontab_tasks.create_task import CreateRunTaskCronTab

cron = CreateRunTaskCronTab()
tasks = ('forex_data_1min_acquisition', 'forex_data_daily_acquisition',
         'stock_data_1min_acquisition', 'stock_data_daily_acquisition')
         
for module in tasks:
    job = cron.add_daily_task(module)
cron.write()
