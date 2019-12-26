import DBAV
import DataAcquistion

class ControllerAV:
    companies_default=['TWTR','ATVI', 'ADBE', 'AMD', 'ALGN', 'ALXN', 'AMZN', 'AMGN', 'AAL', 'ADI', 'AAPL', 'AMAT', 'ASML', 'ADSK', 'ADP',
 'AVGO', 'BIDU', 'BIIB', 'BMRN', 'CDNS', 'CELG', 'CERN', 'CHKP', 'CHTR', 'CTRP', 'CTAS', 'CSCO', 'CTXS', 'CMCSA', 'COST', 
 'CSX', 'CTSH', 'DLTR', 'EA', 'EBAY', 'EXPE', 'FAST', 'FB', 'FISV', 'GILD', 'GOOG', 'GOOGL', 'HAS', 'HSIC', 'ILMN', 'INCY', 
 'INTC', 'INTU', 'ISRG', 'IDXX', 'JBHT', 'JD', 'KLAC', 'KHC', 'LRCX', 'LBTYA', 'LBTYK', 'LULU', 'MELI', 'MAR', 'MCHP', 'MDLZ',
  'MNST', 'MSFT', 'MU', 'MXIM', 'MYL', 'NTAP', 'NFLX', 'NTES', 'NVDA', 'NXPI', 'ORLY', 'PAYX', 'PCAR', 'BKNG', 'PYPL', 'PEP',
   'QCOM', 'REGN', 'ROST', 'SIRI', 'SWKS', 'SBUX', 'SNPS', 'TTWO', 'TSLA', 'TXN', 'TMUS', 'ULTA', 'UAL', 'VRSN', 'VRSK',
    'VRTX', 'WBA', 'WDC', 'WDAY', 'WYNN', 'XEL', 'XLNX']

    def __init__(self,companies=companies_default,error_companies=[],collection='NASDAQ100',filter={'_id':'status'},reset=False):
        #self.filter=filter
        #self.errorcompanies=error_companies
        self.collection=collection
        #self.companies=companies
        self._UpdateCompaniesInfo(id='status',valid_companies=companies,error_companies_recent=error_companies)
        self._DB=DBAV.DBaseAV()

        if reset:
            self.update_valid_companies(data=self.info,collection=self.collection)

        self._acquisition=DataAcquistion.take()
        self._acquisition.update_companies(collection=collection,filter=filter,field='valid_companies')
        self._RunTime()
        
    def update_valid_companies(self,data,collection,filter={'_id':'status'}):
        self._DB.update_companies(data=data,collection=collection,filter=filter)

    def _UpdateCompaniesInfo(self,valid_companies,error_companies_recent,id='status'):
        self.info={'_id':id,'valid_companies':valid_companies,'error_companies_recent':error_companies_recent}

    def _RunTime(self):
        try:
            self._acquisition.run()
            
        except ValueError:
            print(self._acquisition.dict_errors)
            #self.errorcompanies=list(self._acquisition.dict_errors)
            #self.companies=list(self._acquisition.response)
            self._UpdateCompaniesInfo(valid_companies=list(self._acquisition.response),error_companies_recent=list(self._acquisition.dict_errors))
            self._acquisition.reset_list_response()
            print(self.info)
            self.update_valid_companies(data=self.info,collection=self.collection)
            self._acquisition.update_companies(collection=self.collection,field='error_companies_recent',filter={'_id':'status'})
            self._acquisition.run()


ControllerAV()