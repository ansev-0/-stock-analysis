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




class CompanyReader:
    '''This class accepts a list of dictionaries (companies_list)
     It get a url and use the getCompany object to make requests to the API'''

    def __init__(self):
        self.__GetCompany=GetCompany()




    def read(self, companies_list):

        def CheckStringValues(company):
            for value in company.values():
                if not ( isinstance(value,str) ):
                    return False
            return True

        self._Output_list_Json = []
        
        header='https://www.alphavantage.co/query?'

        
        load_dict={'function':'TIME_SERIES_INTRADAY',
                   'symbol':'',
                   'interval':'1min',
                   'outputsize':'full',
                   'datatype':'json',
                   'apikey':'O39L8VIVYYJYUN3P'}
            
        
        if not companies_list:
            self._Output_list_Json.append({'Error':{'Error empty': 'empty list has been passed'}})

        else:

            for company in companies_list:
                if company.keys() != load_dict.keys():
                    self._Output_list_Json.append({'Error': {'Error keys': 'Missing or Invalid keys'}})
                else:
                    
                    if CheckStringValues(company):
                        load_dict.update(company)
                        url = header+( ''.join([f'&{x}={y}'.format(x,y) for x,y in load_dict.items()])[1:] )
                        for i in np.arange(3):
                            
                            try:
                                print('Trying connect with API alphavantage ...')
                                out=self.__GetCompany.get(url)
                                if len(out)<2 or isinstance(out,str):
                                    raise ValueError('Failed response')
                                self._Output_list_Json.append(out)
                                print('Connect successfully')
                                break
                            except Exception:
                                print('Connect failed trying again ...')
                                if i==2:
                                    self._Output_list_Json.append({'Error':{'Error connect':{'url':url,'company parameters':company}}})
                                    print("it was not possible to establish connection")
                                    break
                                time.sleep(60)
                        

                    else:
                        self._Output_list_Json.append({'Error String': 'Any value is not str'})
        return self._Output_list_Json



######################################################
#Object Constructor
def Reader():
    return CompanyReader()


    



        

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
    



  







    
