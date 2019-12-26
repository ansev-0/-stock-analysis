#                   Libraries to test

#TEST
import unittest

#############
import pandas as pd
import numpy as np
import sqlite3
import urllib.request, json 
from datetime import datetime
import time

from Reader import Reader

#comments:

#it could have be updated in the future: 

#        elif value.isnumeric():
#           raise ValueError(f'String mustnt be numeric')


class AVdict:
    def __init__(self):
        self.dict_AV={'function':'TIME_SERIES_INTRADAY',
                   'symbol':'',
                   'interval':'1min',
                   'outputsize':'full',
                   'datatype':'json',
                   'apikey':'O39L8VIVYYJYUN3P'}

class BuilderDict(AVdict):

    def __init__(self):
        self._reset_output_list_dict()
        super().__init__()

    
#Public method of instance


    def build(self,data,frecuency=False,function='TIME_SERIES_INTRADAY',outputsize='full'):
        self._reset_output_list_dict()
        self.dict_AV.update({'function':function,'outputsize':outputsize})
        if frecuency:
            self._CompanyFrecuency(data)
        else:
            self._Company(data)
        return self._output_list_dicts


#private method of instance

    def _CheckStringTypeItem(self,value):
        if not isinstance(value,str):
            raise TypeError(f'Items mus be str: {value}')
        elif value.isnumeric():
            raise ValueError(f'String mustnt be numeric')
            

    def _reset_output_list_dict(self):
        self._output_list_dicts=[]

    def _AddDictToList(self,symbol,interval='1min'):
        
        self.dict_AV.update(
            {'symbol':symbol,
             'interval':interval})
        self._output_list_dicts.append(self.dict_AV.copy())
        
        
             
            
    def _Company(self,data):
        if isinstance(data,list) or isinstance(data,tuple):
            for value in data:
                self._CheckStringTypeItem(value)
                self._AddDictToList(symbol=value)
                
                
    def _CompanyFrecuency(self,data):

        def ChecktoAddTuple(tup):
            if len(tup) != 2:
                raise ValueError (f'length of tuple mus be 2, paased= {tup}')
            else:
                self._CheckStringTypeItem(tup[0])
                self._CheckStringTypeItem(tup[1])
                self._AddDictToList(symbol=tup[0],interval=tup[1])
                

        if isinstance(data,list):
            for tup in data:
                if not isinstance (tup,tuple):
                    raise TypeError(f'the items on the list must be a tuple, argument invalid : {tup}')
                else:
                    ChecktoAddTuple(tup)

        elif isinstance(data,dict):
             for key,value in data.items():
                self._CheckStringTypeItem(key)
                self._CheckStringTypeItem(value)
                self._AddDictToList(symbol=key,interval=value)

        elif isinstance(data,tuple):
            ChecktoAddTuple(data)

        else:
            raise TypeError (f'Invalid type: {type(data)}, you must pass a list of tuple or tuple or dict')

        
BuilderDict=BuilderDict()

#Test BuilderDictClass
# class TestBuilderDict(unittest.TestCase):


#     def setUp(self):
#         self.load_dict={'function':'TIME_SERIES_INTRADAY',
#                    'symbol':'',
#                    'interval':'1min',
#                    'outputsize':'full',
#                    'datatype':'json',
#                    'apikey':'O39L8VIVYYJYUN3P'}
#         self.load_dict2=self.load_dict.copy()
#         self.Builder=BuilderDict()


#     def test_frecuency_tuple(self):
#         self.load_dict['symbol']='TWTR'
#         self.load_dict['interval']='1min'
        
#         self.assertEqual(self.Builder.build(frecuency=True,data=('TWTR','1min')), [self.load_dict])

#     def test_frecuency_listoftuple(self):
#         self.load_dict['symbol']='TWTR'
#         self.load_dict['interval']='1min'
#         self.load_dict2['symbol']='AAPL'
#         self.load_dict2['interval']='3min'
#         self.assertCountEqual(self.Builder.build(frecuency=True,data=[('TWTR','1min'),('AAPL','3min')]), [self.load_dict,self.load_dict2])

#     def test_frecuency_dict(self):
#         self.load_dict['symbol']='TWTR'
#         self.load_dict['interval']='1min'
#         self.load_dict2['symbol']='AAPL'
#         self.load_dict2['interval']='3min'
#         self.assertEqual(self.Builder.build(frecuency=True,data={'TWTR':'1min','AAPL':'3min'}), [self.load_dict,self.load_dict2])

#     def test_frecuency_list_strings(self):
#         with self.assertRaises(TypeError):
#             self.Builder.build(frecuency=True,data=['TWTR','AAPL'])

#     def test_frecuency_dict_value_numeric(self):
#         with self.assertRaises(TypeError):
#             self.Builder.build(frecuency=True,data={'TWTR',2})

#     def test_frecuency_dict_key_numeric(self):
#         with self.assertRaises(TypeError):
#             self.Builder.build(frecuency=True,data={2,'2'})

#     def test_frecuency_list_of_tup_numeric(self):
#         with self.assertRaises(TypeError):
#             self.Builder.build(frecuency=True,data=[(2,'2')])

#     def test_frecuency_tup_numeric(self):
#         with self.assertRaises(TypeError):
#             self.Builder.build(frecuency=True,data=(2,'2'))

#     def test_frecuency_tup_str_numeric(self):
#         with self.assertRaises(ValueError):
#             self.Builder.build(frecuency=True,data=('2','h'))

#     def test_no_frecuency_list_strings(self):
#         self.load_dict['symbol']='TWTR'
#         self.load_dict['interval']='1min'
#         self.load_dict2['symbol']='AAPL'
#         self.load_dict2['interval']='1min'
#         self.assertEqual(self.Builder.build(frecuency=False,data=['TWTR','AAPL']), [self.load_dict,self.load_dict2])



if __name__ == '__main__':
    unittest.main()


#     def test_companies_list_empty(self):
#         with self.assertRaises(ValueError):
#             self.reader.read([])