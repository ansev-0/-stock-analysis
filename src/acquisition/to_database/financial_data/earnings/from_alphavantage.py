from src.acquisition.to_database.financial_data.from_alphavantage import UpdateFinancialFeatureAlphaVantage
from src.acquisition.to_database.save_many_stock_collection import UpdateManyStockData


class UpdateEarningsAlphaVantage(UpdateFinancialFeatureAlphaVantage):
    '''
    This class is an interface to save the EARNINGS data of the Alphavantage API

    Parameters
    ----------

    apikey: str.
        key of API Alphavantage.

    new_database: str
        valid parameters = 'create' and 'not create'

    '''
    
    feature = 'earnings'
    _ADD_TYPE = feature.capitalize()

class UpdateEarningsAlphaVantageMany(UpdateEarningsAlphaVantage, UpdateManyStockData):
    pass
        
