from src.crontab_tasks.create_task import CreateRunTaskCronTab
from src.tools.path import get_financial_path
import json, os

cron = CreateRunTaskCronTab()



tasks = (
         'forex_data_1min_acquisition.py', 
         'forex_data_daily_acquisition.py',
         'stock_data_1min_acquisition.py',
         'stock_data_daily_acquisition.py', 
         'balance_sheet_acquisition.py', 
         'cash_flow_acquisition.py', 
         'earnings_acquisition.py', 
         'income_statement_acquisition.py',
         'overview_acquisition.py'
         )



with open(os.path.join(get_financial_path(), 'config.json')) as file:
    password = json.load(file)['password']

init_mongo = cron.new(command=f'sleep 60 && echo {password} | sudo -S -k mongod --dbpath /var/log/mongodb')
init_mongo.every_reboot()
cron.add_every_minute_task(15, 'twitter_status.py')

for module in tasks:
    job = cron.add_daily_task(module)
    job_reebot = cron.add_reboot_task(module)
cron.write()
