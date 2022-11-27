import os
from src.acquisition.to_database.forex_data.save_from_api import SaveForexDataFromApi
from src.crontab_tasks.task_manager import TaskManager

def get_forex_data_daily_alphavantage():
    manager = TaskManager(attemps=3)
    manager(os.path.basename(__file__), 
            lambda *args: SaveForexDataFromApi.daily_alphavantage(frecuency='1min')\
                                              .save_reporting_errors(attemps=2))
    return 'Done func'

