from src.acquisition.acquisition.alphavantage.alphavantage import AlphaVantage 

class FundamentalData(AlphaVantage):
    '''

    This class is used to get Fundamental data from Alphavantage API.
    Api reference: https://www.alphavantage.co/documentation/##fundamentals.

    '''

    @AlphaVantage._get_data
    def get_company_overview(self, symbol):
        FUNCTION = 'OVERVIEW'
        return symbol, FUNCTION

    @AlphaVantage._get_data
    def get_income_statement(self, symbol):
        FUNCTION = 'INCOME_STATEMENT'
        return symbol, FUNCTION

    @AlphaVantage._get_data
    def get_cash_flow(self, symbol):
        FUNCTION = 'CASH_FLOW'
        return symbol, FUNCTION

    @AlphaVantage._get_data
    def get_earnings(self, symbol):
        FUNCTION = 'EARNINGS'
        return symbol, FUNCTION

    @AlphaVantage._get_data
    def listing_status(self, date, state):
        FUNCTION = 'LISTING_STATUS'
        return date, state, FUNCTION

