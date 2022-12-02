import os
from src.acquisition.to_database.stock_data.save_from_api import SaveStockDataFromApi
from src.crontab_tasks.task_manager import TaskManager

def get_stock_data_daily_alphavantage():
    manager = TaskManager(attemps=3)
    manager(os.path.basename(__file__), 
                    lambda *args: SaveStockDataFromApi.dailyadj_alphavantage()\
                                                      .save_reporting_errors(attemps=2))
    return 'Done func'

