from src.acquisition.to_database.twitter_db.searchs_asset.jobs.status import UpdateStatusFromAPI
from src.crontab_tasks.task_manager import TaskManager
import os

def twitter_status():
    manager = TaskManager(attemps=3, freq='0 days 00:10:00')
    manager(os.path.basename(__file__), 
            lambda *args: UpdateStatusFromAPI()())

#if __name__ == '__main__':
#    twitter_status()
