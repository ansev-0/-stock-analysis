import pandas as pd
import numpy as np
import urllib.request, json 
import requests
from datetime import datetime
import time
import timeit
from acquisition.errors_response import check_errors_alphavantage

class ReaderAlphaVantage: 

    def __init__(self,attemps=3,delays = [60,10]):
        self.config(attemps,delays)
        self.test_response = check_errors_alphavantage.ErrorsResponseApi_Alphavantage()


    def _get_transform_function(self,frame):
        if frame:
            return self._to_frame
        else:
            return lambda *args,**kwards: kwards['dictionary']
            
    def _to_frame(self,dictionary,dt,ascending,query_function):

        df = (pd.DataFrame.from_dict(dictionary)
                .T
                .astype(float))
        df.columns = ['Open','High','Low','Close','Volume']

        if dt: 
            df.index=pd.to_datetime(df.index)
        if ascending:
            df=df.sort_index()

        return df


                                                                
    def config(self,attemps=3,delays = [60,10]):
        self.attemps = attemps
        self.delays = delays


    def read(
        self,
        queries,
        frame=False,
        dt=False,
        ascending = True
    ):
        ''' 
        This function returns two dictionaries, one of them contains the time series (values) for each company (keys),
        the values ​​will be a dictionary (with frame = False) or a DataFrame (frame = True).
        The second dictionary contains the errors, there will be a field for company (keys)

        Parameters
        ----------

        queries : tuple,list or dict
            API request, list or tuple of dictionaries or a dictionary.

        frame: bool
            True if the output format must be a DataFrame, otherwise it returns a dictionary

        dt: bool
            Only valid if frame = True, if dt = True, the index DataFrame is DateTime.

        ascending: bool
            Only valid if frame = True and dt = True. The dataframe sort the index upwards.
            That is in chronological order. The first row corresponds to the earliest date
        '''
        
        if isinstance(queries, list) or isinstance(queries,tuple):
            list_queries = queries 
        elif isinstance(queries,dict):
            list_queries = [queries]
        format_output = self._get_transform_function(frame)
        dict_valids={}
        dictErrors={}

        for query in list_queries:
            symbol = query['symbol']
            count_attemps = 0
            while(count_attemps < self.attemps):

                try:
                    response = requests.get('https://www.alphavantage.co/query', params=query)

                except requests.exceptions.RequestException as error:  
                    print (error)
                else:

                    json = response.json() 
                    count_attemps+=1 #attemp n

                    try:
                        self.test_response.pass_test(json,query)

                    except ValueError:

                        if count_attemps == self.attemps:
                            dictErrors[symbol]=[query,json.copy(),response.staus_code]
                        else:
                            time.sleep(self.delays[count_attemps-1])
                    else:
                        
                        dict_valids[symbol] = format_output(dictionary = json[list(json)[1]],
                                                            dt = dt,
                                                            ascending = ascending) #save useful data
                        print('{}'.format(symbol))
                        break

        return dict_valids, dictErrors






                        

