from src.acquisition.to_database.financial_data.from_alphavantage import UpdateFinancialFeatureAlphaVantage
from src.acquisition.to_database.save_many_stock_collection import UpdateManyStockData


class UpdateIncomeStatementAlphaVantage(UpdateFinancialFeatureAlphaVantage):
    '''
    This class is an interface to save the INCOME STATEMENT data of the Alphavantage API

    Parameters
    ----------

    apikey: str.
        key of API Alphavantage.

    new_database: str
        valid parameters = 'create' and 'not create'

    '''

    feature = 'income_statement'


class UpdateIncomeStatementAlphaVantageMany(UpdateIncomeStatementAlphaVantage, UpdateManyStockData):
    pass


        