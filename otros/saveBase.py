from DataAV import DataAV as av
import numpy as np
import time
labels=['TWTR','ATVI', 'ADBE', 'AMD', 'ALGN', 'ALXN', 'AMZN', 'AMGN', 'AAL', 'ADI', 'AAPL', 'AMAT', 'ASML', 'ADSK', 'ADP',
 'AVGO', 'BIDU', 'BIIB', 'BMRN', 'CDNS', 'CELG', 'CERN', 'CHKP', 'CHTR', 'CTRP', 'CTAS', 'CSCO', 'CTXS', 'CMCSA', 'COST', 
 'CSX', 'CTSH', 'DLTR', 'EA', 'EBAY', 'EXPE', 'FAST', 'FB', 'FISV', 'GILD', 'GOOG', 'GOOGL', 'HAS', 'HSIC', 'ILMN', 'INCY', 
 'INTC', 'INTU', 'ISRG', 'IDXX', 'JBHT', 'JD', 'KLAC', 'KHC', 'LRCX', 'LBTYA', 'LBTYK', 'LULU', 'MELI', 'MAR', 'MCHP', 'MDLZ',
  'MNST', 'MSFT', 'MU', 'MXIM', 'MYL', 'NTAP', 'NFLX', 'NTES', 'NVDA', 'NXPI', 'ORLY', 'PAYX', 'PCAR', 'BKNG', 'PYPL', 'PEP',
   'QCOM', 'REGN', 'ROST', 'SIRI', 'SWKS', 'SBUX', 'SYMC', 'SNPS', 'TTWO', 'TSLA', 'TXN', 'TMUS', 'ULTA', 'UAL', 'VRSN', 'VRSK',
    'VRTX', 'WBA', 'WDC', 'WDAY', 'WYNN', 'XEL', 'XLNX']
not_exist=[]
class saveBase:
    def __init__(self,labels):
        self.labels=labels

    def save(self):
       self.not_exist=[]
       for key in self.labels:
           for i in np.arange(3):
               try:
                   av(symbol=key).to_sqlbase()
                   print('Save Actions with ' + key+ ' in Base Successffully')
                   break
               except:
                   print(' Save Actions failed with company: ',key,' waited...',i)
                   if i==2:
                         print("120s...." ,key," dont! exists!")
                         self.not_exist.append(key)
                         break
                   time.sleep(60)
    def drop(self):
        for key in self.labels:
            try:
                av(symbol=key).drop_all()
                print('Drop data of company ',key,' succesfdully')
            except:
                print('there arent values of company ',key)

saveBase(labels).drop()
saveBase(labels).save()
saveBase(labels).save()
