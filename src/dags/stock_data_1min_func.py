import os
from src.acquisition.to_database.stock_data.save_from_api import SaveStockDataFromApi
from src.crontab_tasks.task_manager import TaskManager

def get_stock_1min_alphavantage():
    manager = TaskManager(attemps=3)
    manager(os.path.basename(__file__),
            lambda *args: SaveStockDataFromApi.intraday_alphavantage(frecuency='1min')\
                                                  .save_reporting_errors(attemps=2))
    return 'Done func'

#if __name__ == '__main__':
#    get_stock_1min_alphavantage()
    