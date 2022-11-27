import os
from src.acquisition.to_database.financial_data.save_from_api import SaveFinancialDataFromApi
from src.crontab_tasks.task_manager import TaskManager

def get_income_statements_alphavantage():
    manager = TaskManager(attemps=3, freq='25 days 00:00:00')
    manager(os.path.basename(__file__), 
            lambda *args: SaveFinancialDataFromApi.income_statement_alphavantage()\
                                                  .save_reporting_errors(attemps=2))
    return 'Done func'



