import pandas as pd
import numpy as np
import sqlite3
import urllib.request, json 
from datetime import datetime
import time

#----------------------------------------------Alpha/Base Vantage object-------------------------------------------------
class GetCompany: 
    def get(self,url):
        ''' This function returns the Json received'''
        with urllib.request.urlopen(url) as url:
            return json.loads(url.read().decode())




class CompanyReader(GetCompany):
    '''This class accepts a list of dictionaries (companies_list)
     It get a url and use the getCompany object to make requests to the API'''

    def __init__(self,attempts,delay_error):

        self.attempts = attempts
        self.delay_error = delay_error




    def read(self, companies_list):

        def CheckStringValues(company):
            for value in company.values():
                if not ( isinstance(value,str) ):
                    return False
            return True

        Output_list_Json = []
        
        header='https://www.alphavantage.co/query?'

        
        load_dict={'function':'TIME_SERIES_INTRADAY',
                   'symbol':'',
                   'interval':'1min',
                   'outputsize':'full',
                   'datatype':'json',
                   'apikey':'O39L8VIVYYJYUN3P'}
            
        
        if not companies_list:
            Output_list_Json.append({'Error':{'Error empty': 'empty list has been passed'}})

        else:

            for company in companies_list:
                if company.keys() != load_dict.keys():
                    Output_list_Json.append({'Error': {'Error keys': 'Missing or Invalid keys'}})
                else:
                    
                    if CheckStringValues(company):

                        load_dict.update(company)
                        url = header+( ''.join([f'&{x}={y}'.format(x,y) for x,y in load_dict.items()])[1:] )
                        symbol = load_dict['symbol']

                        for i in range(self.attempts):

                            try:
                                print(f'Trying connect with API alphavantage, company: {symbol}...')
                                out=self.get(url)
                                if len(out)<2 or isinstance(out,str):
                                    raise ValueError('Failed response')
                                else:
                                    Output_list_Json.append(out)
                                    print('Connect successfully')
                                    break
                            except Exception:
                                print('Connect failed trying again ...')
                                if i==self.attempts-1:
                                        Output_list_Json.append({'Error':{'Error connect':{'url':url,'company parameters':company}}})
                                        print("it was not possible to establish connection")
                                        break
                                time.sleep(self.delay_error)
                        

                    else:
                            Output_list_Json.append({'Error':{'Error String': 'Any value is not str'}})
        return Output_list_Json



######################################################
#Object Constructor
def Reader(attempts,delay_error):
    return CompanyReader(attempts=attempts,delay_error = delay_error)


    



        

########################################################################################
         

# import unittest
# class TestCompanyReader(unittest.TestCase):
#     def setUp(self):
#         self.reader=CompanyReader()


#     def test_list_json_valid(self):
#         self.list_dict=[{'function':'TIME_SERIES_INTRADAY',
#             'symbol':'TWTR',
#             'interval':'1min',
#             'outputsize':'full',
#             'datatype':'json',
#             'apikey':'O39L8VIVYYJYUN3P'}]
#         self.assertTrue(self.reader.read(self.list_dict))
    
#     def test_companies_list_empty(self):
#         with self.assertRaises(ValueError):
#             self.reader.read([])
    


        
            
# if __name__ == '__main__':
#     unittest.main()
    



  







    
