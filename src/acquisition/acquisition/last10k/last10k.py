from functools import wraps
import time
from src.acquisition.acquisition.reader import Reader
from src.acquisition.acquisition.last10k.apikey import ApiKey
from src.tools.mappers import switch_none


class Last10K:

    '''
    This class is used to get data from
    https://dev.last10k.com/

    '''
    _LAST_10K_URL = 'https://services.last10k.com/v1/company/'

    def __init__(self, apikey, delays=None, **kwargs):
        self.apikey = apikey
        self.config(delays)
        self._reader = Reader(**kwargs)

    def config(self, delays=None):
        self.delays = switch_none(delays, [60, 20])
        self.attemps = len(self.delays) + 1


    @classmethod
    def _get_data(cls, func):

        @wraps(func)
        def read_url(self, company, *args, **kwargs):

            query_params = func(self, *args, **kwargs)
            params={}

            if isinstance(query_params, tuple):
                self._reader.base_url = self._LAST_10K_URL + '/'.join([company, query_params[0]])
                params = query_params[1]

            elif isinstance(query_params, str):
                self._reader.base_url = self._LAST_10K_URL + '/'.join([company, query_params])

            elif not query_params:
                self._reader.base_url = self._LAST_10K_URL + company

            elif isinstance(query_params, dict):
                self._reader.base_url = self._LAST_10K_URL + company
                params = query_params

                
            return self._reader.read(auth=ApiKey(self.apikey), query=params)
            

        return read_url

    

class BalanceSheet(Last10K):
    @Last10K._get_data
    def get(self, form_type, filing_order):
        return 'balancesheet', {'formType' : form_type, 'filingOrder' : filing_order}


reader = BalanceSheet('130e21c2408c4af6ba4ea38b2ff259aa')
r = reader.get(company='twtr', form_type='10-K', filing_order=0)

print(r.json())


class DocumentAndEntitySummary(Last10K):
    @Last10K._get_data
    def get(self, form_type, filing_order):
        return {'formType' : form_type, 'filingOrder' : filing_order}


class CashFlows(Last10K):
    @Last10K._get_data
    def get(self, form_type, filing_order):
        return 'cashflows', {'formType' : form_type, 'filingOrder' : filing_order}



reader = CashFlows('130e21c2408c4af6ba4ea38b2ff259aa')
r = reader.get(company='twtr', form_type='10-K', filing_order=0)

print(r.json())

