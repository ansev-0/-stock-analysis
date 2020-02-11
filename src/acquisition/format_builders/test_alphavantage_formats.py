import alphavantage_formats
import requests
import unittest
import pandas as pd
from src.tools.builders import inlist


class CheckDataFrame(unittest.TestCase):
    
    def setUp(self):
        self.df = pd.DataFrame()

    def check_columns(self,expected_columns):
        self.assertCountEqual(expected_columns, self.df.columns.tolist())

    def check_index_type(self,expected_type):
        self.assertTrue(isinstance(self.df.index, expected_type)) 

    def check_value_in_index(self,value,is_in):
        if is_in:
            self.assertTrue(value in self.df.index) 
        else:
            self.assertTrue(value not in self.df.index) 

    def check_data_type(self,expected_types):
        expected_types = inlist(expected_types)

        data_types = [str(typ) for typ in self.df.dtypes]
        self.assertCountEqual(expected_types,data_types)

    def check_ascending_index(self,ascending):
        index_serie = self.df.index.to_series()
        self.assertTrue(index_serie.equals(index_serie.sort_values(ascending = ascending)))


class Test_Alphavantage_Formats_build_frame(CheckDataFrame):


    def setUp(self):
        APIKEY = 'demo'
        SYMBOL = 'MSFT'
        #dictionary of queries
        self.queries = {'TIME_SERIES_INTRADAY':{'function':'TIME_SERIES_INTRADAY',
                                           'symbol':SYMBOL,
                                           'interval':'5min',
                                           'apikey':APIKEY},
                        'GLOBAL_QUOTE':{'function':'GLOBAL_QUOTE',
                                        'symbol':SYMBOL,
                                        'apikey':APIKEY},
                        'SYMBOL_SEARCH':{'function':'SYMBOL_SEARCH',
                                         'keyworkds':'BA',
                                         'apikey':APIKEY},
                        'CURRENCY_EXCHANGE_RATE':{'function':'CURRENCY_EXCHANGE_RATE',
                                                  'from_currency':'USD',
                                                  'to_currency':'JPY',
                                                  'apikey':APIKEY}
          
        }
        #Getting json
        self.json_dict={k:requests.get('https://www.alphavantage.co/query',params = v).json() for k,v in self.queries.items()}
        #Creating object to test.
        self.builder_formats = alphavantage_formats.FormatBuilderAlphavantage()

    def test_timeseries_intraday(self):

        default_query = {'json':self.json_dict['TIME_SERIES_INTRADAY'],
                         'query':self.queries['TIME_SERIES_INTRADAY']}

        #test default query
        self.df = self.builder_formats.build_frame(**default_query)
        self.check_columns(['open','high','low','close','volume'])
        self.check_index_type(pd.DatetimeIndex)
        self.check_data_type(['float64']*5)
        self.check_ascending_index(ascending = True)

        #test with enumerate_axis = True
        self.df = self.builder_formats.build_frame(**dict(default_query,**{'enumerate_axis':True}))
        self.check_columns(['1. open','2. high','3. low','4. close','5. volume'])

        
        #test with ascending = False
        self.df = self.builder_formats.build_frame(**dict(default_query,**{'ascending':False}))
        self.check_ascending_index(ascending = False)

        #test with pd.to_datetime = False
        self.df = self.builder_formats.build_frame(**dict(default_query,**{'to_datetime':False}))
        self.check_index_type(object)

        #Test with datatype = str
        self.df = self.builder_formats.build_frame(**dict(default_query,**{'datatype':str}))
        self.check_data_type(['object']*5)


#    def test_global_quote(self):
#        df = self.builder_formats.build_frame(json = self.json_dict['GLOBAL_QUOTE'],
#                                              query = self.queries['GLOBAL_QUOTE'])
#        #Lengh and Names of columns
#        self.assertCountEqual([1,['Global Quote']],[len(df.columns),[*df.columns]])
#

                                      
                                             

if __name__ == '__main__':
    unittest.main()