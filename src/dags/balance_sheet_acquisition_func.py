from src.acquisition.to_database.financial_data.save_from_api import SaveFinancialDataFromApi
from src.crontab_tasks.task_manager import TaskManager
import os

def get_balance_sheet_alphavantage():
    manager = TaskManager(attemps=3, freq='25 days 00:00:00')
    manager(os.path.basename(__file__), 
                lambda *args: SaveFinancialDataFromApi.balance_sheet_alphavantage()\
                        .save_reporting_errors(attemps=2))
    return 'Done func'

        

