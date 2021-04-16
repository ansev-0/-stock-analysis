from src.acquisition.to_database.save_from_api import SaveDataFromApi
from src.view.acquisition.to_database.financial_data.show_status.status_save_financial_data import SaveFinancialDataShowStatus
from src.acquisition.to_database.financial_data.errors.check_save_from_api \
    import CheckErrorsSaveFinancialDataFromApi
from src.acquisition.to_database.financial_data.company_overview.from_alphavantage import UpdateOverviewAlphaVantageMany
from src.acquisition.to_database.financial_data.cash_flow.from_alphavantage import UpdateCashFlowAlphaVantageMany
from src.acquisition.to_database.financial_data.balance_sheet.from_alphavantage import UpdateBalanceSheetAlphaVantageMany
from src.acquisition.to_database.financial_data.earnings.from_alphavantage import UpdateEarningsAlphaVantageMany
from src.acquisition.to_database.financial_data.income_statement. from_alphavantage import UpdateIncomeStatementAlphaVantageMany

class SaveFinancialDataFromApi(SaveDataFromApi):

    def __init__(self, api, collection, data_collector):

        self._check_errors = CheckErrorsSaveFinancialDataFromApi(api=api, collection=collection)
        super().__init__(api, collection, data_collector)
        self.api = api
        self._show_status=SaveFinancialDataShowStatus()

    @property
    def check_errors(self):
        return self._check_errors

    @property
    def show_status(self):
        return self._show_status

    @classmethod
    def cash_flow_alphavantage(cls, apikey, **kwargs):
        class_collector = cls.__get_cash_flow_collector('alphavantage')
        return cls(api='alphavantage',
                   data_collector=class_collector(apikey=apikey, **kwargs),
                   collection='cash_flow')

    @classmethod
    def balance_sheet_alphavantage(cls,  apikey, **kwargs):
        class_collector = cls.__get_balance_sheet_collector('alphavantage')
        return cls(api='alphavantage',
                   data_collector=class_collector(apikey=apikey, **kwargs),
                   collection='balance_sheet')

    @classmethod
    def overview_alphavantage(cls, apikey, **kwargs):
        class_collector = cls.__get_overview_collector('alphavantage')
        return cls(api='alphavantage',
                   data_collector=class_collector(apikey=apikey, **kwargs),
                   collection='overview')

    @classmethod
    def income_statement_alphavantage(cls, apikey, **kwargs):
        class_collector = cls.__get_income_statement_collector('alphavantage')
        return cls(api='alphavantage',
                   data_collector=class_collector(apikey=apikey, **kwargs),
                   collection='income_statement')

    @classmethod
    def earnings_alphavantage(cls, apikey, **kwargs):
        class_collector = cls.__get_earnings_collector('alphavantage')
        return cls(api='alphavantage',
                   data_collector=class_collector(apikey=apikey, **kwargs),
                   collection='earnings')

    @classmethod
    def __get_cash_flow_collector(cls, api):
        return {'alphavantage' : UpdateCashFlowAlphaVantageMany}[api]

    @classmethod
    def __get_overview_collector(cls, api):
        return {'alphavantage' : UpdateOverviewAlphaVantageMany}[api]

    @classmethod
    def __get_earnings_collector(cls, api):
        return {'alphavantage' : UpdateEarningsAlphaVantageMany}[api]

    @classmethod
    def __get_balance_sheet_collector(cls, api):
        return {'alphavantage' : UpdateBalanceSheetAlphaVantageMany}[api]

    @classmethod
    def __get_income_statement_collector(cls, api):
        return {'alphavantage' : UpdateIncomeStatementAlphaVantageMany}[api]

