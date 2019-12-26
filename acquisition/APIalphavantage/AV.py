from .InterfaceObjects import Reader,Builder
import pandas as pd
import datetime


class InterfaceAV:
    def __init__(self):
        self._Builder=Builder.Builder()
        self._Reader=Reader.Reader(3,60)

    #Private Methods of instance


    def _CheckTypeBool(self,parameter):
        if not (isinstance(parameter,bool)):
            raise TypeError(f'{parameter} must be bool')


    def _Convert(self,json,dt=False,ascending=True,df=False):
        new_data=json[list(json)[-1]] #get the content of the last key
        if df:
            
            df=pd.DataFrame.from_dict(new_data).T.astype(float).rename(columns={'1. open':'Open','2. high':'High','3. low':'Low','4. close':'Close','5. volume':'Volume'})
            if dt:
                df.index=pd.to_datetime(df.index)
            if ascending:
                df=df.sort_index()
            return df
        else:
            return new_data

    #   Public method of instance
    
    def read(self,data,frecuency=False,dt=False,function='TIME_SERIES_INTRADAY',outputsize='full',df=True,container='list',ascending=True):
        self._CheckTypeBool(ascending)
        self._CheckTypeBool(dt)
        self._CheckTypeBool(df)
        self._CheckTypeBool(frecuency)

        if (container != 'list') and (container != 'dict'):
            raise ValueError('container must be dict or list')
    
        list_of_dicts=self._Builder.build(data,frecuency=frecuency,function=function,outputsize=outputsize)
        list_of_response=self._Reader.read(list_of_dicts)

        list_of_response=[self._Convert(json,dt=dt,ascending=ascending,df=df) for json in list_of_response]
        if container == 'dict':
            symbols=data.copy()

            if frecuency:
                symbols=[]
                if isinstance(data,list):
                    for tup in data:
                        if isinstance(tup,tuple):
                            symbols.append(tup[0])
                        else:
                            raise TypeError('You must pass a list of tuple, a dict or a tuple')

                elif isinstance(data,dict):
                    symbols=data.keys()

                elif isinstance(data,tuple):
                    symbols.append(data[0])
            return dict(zip(symbols,list_of_response))

        else:
            return list_of_response
        
def Interface():
    return InterfaceAV()


#reader=Interface()

# companies=['TWTR','ATVI', 'ADBE', 'AMD', 'ALGN', 'ALXN', 'AMZN', 'AMGN', 'AAL', 'ADI', 'AAPL', 'AMAT', 'ASML', 'ADSK', 'ADP',
#                     'AVGO', 'BIDU', 'BIIB', 'BMRN', 'CDNS', 'CELG', 'CERN', 'CHKP', 'CHTR', 'CTRP', 'CTAS', 'CSCO', 'CTXS', 'CMCSA', 'COST', 
#                     'CSX', 'CTSH', 'DLTR', 'EA', 'EBAY', 'EXPE', 'FAST', 'FB', 'FISV', 'GILD', 'GOOG', 'GOOGL', 'HAS', 'HSIC', 'ILMN', 'INCY', 
#                     'INTC', 'INTU', 'ISRG', 'IDXX', 'JBHT', 'JD', 'KLAC', 'KHC', 'LRCX', 'LBTYA', 'LBTYK', 'LULU', 'MELI', 'MAR', 'MCHP', 'MDLZ',
#                     'MNST', 'MSFT', 'MU', 'MXIM', 'MYL', 'NTAP', 'NFLX', 'NTES', 'NVDA', 'NXPI', 'ORLY', 'PAYX', 'PCAR', 'BKNG', 'PYPL', 'PEP',
#                     'QCOM', 'REGN', 'ROST', 'SIRI', 'SWKS', 'SBUX', 'SYMC', 'SNPS', 'TTWO', 'TSLA', 'TXN', 'TMUS', 'ULTA', 'UAL', 'VRSN', 'VRSK',
#                     'VRTX', 'WBA', 'WDC', 'WDAY', 'WYNN', 'XEL', 'XLNX']

#companies=['TWTR','AAPL','MNST', 'MSFT', 'MU', 'MXIM', 'MYL', 'NTAP', 'NFLX', 'NTES']

#out=reader.read(companies,df=False,container='dict')
#print(out.keys())