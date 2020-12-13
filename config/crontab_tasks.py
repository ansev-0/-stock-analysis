from src.crontab_tasks.create_task import CreateRunTaskCronTab

cron = CreateRunTaskCronTab()

f = open('/home/antonio/financialworks/config.txt')
password = f.read()

#init mongodb
init_mongo = cron.new(command=f'sleep 60 && echo {password} | sudo -S -k mongod --config /etc/mongodb.conf')
init_mongo.every_reboot()

tasks = ('forex_data_1min_acquisition.py', 'forex_data_daily_acquisition.py',
         'stock_data_1min_acquisition.py', 'stock_data_daily_acquisition.py')

for module in tasks:
    job = cron.add_daily_task(module)
    job_reebot = cron.add_reboot_task(module)
cron.write()
