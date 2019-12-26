
#                   Libraries 

import pandas as pd
import numpy as np
import sqlite3
import urllib.request, json 
from datetime import datetime
import time

#------------------------------Alpha/Base Vantage object-------------------------------------------------
class DataAV:
    def __init__(self,function='TIME_SERIES_INTRADAY',symbol='TWTR',interval='1min',outputsize='full',datatype='json',apikey='O39L8VIVYYJYUN3P'):
        self.function=function
        self.symbol=symbol
        self.interval=interval
        self.outputsize=outputsize
        self.datatype=datatype
        self.apikey=apikey
        self.url='https://www.alphavantage.co/query?'+'function='+self.function+'&symbol='+self.symbol+'&interval='+self.interval+'&outputsize='+self.outputsize+'&datatype='+self.datatype+'&apikey='+self.apikey
        self.base="financialbase/"+self.function + self.interval + self.outputsize
        try:
            self.get_lastDate()
        except:
            self.reset_lastDate()


    def get_lastDate(self):
        self.last_time_InBase=self.from_sqlbase(last=True,dt=False).index[-1]


    def reset_lastDate(self):
        self.last_time_InBase= datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    def get(self,format='frame',dt=True):

        with urllib.request.urlopen(self.url) as url:
            self._Json=json.loads(url.read().decode())
            self.last_time=self._Json['Meta Data']['3. Last Refreshed']
        if format=='json':
            return self._Json

        elif format == 'frame':
            self._dfGet=pd.DataFrame([self._Json[key] for key in self._Json][1]).T.astype(float).rename(columns={'1. open':'Open','2. high':'High','3. low':'Low','4. close':'Close','5. volume':'Volume'})
            if dt:
                self._dfGet.index=pd.to_datetime(self._dfGet.index)
            self._dfGet.sort_index(inplace=True)
            return self._dfGet

    def from_sqlbase(self,date=0,rows=False,last=False,dt=True):
        con = sqlite3.connect(self.base)
        if (rows==False) & (last==False):
            query="SELECT * FROM {}".format
            query=query(self.symbol)
        elif last:
            query= "SELECT * FROM {} ORDER BY Time DESC LIMIT 1".format
            query=query(self.symbol)
        elif rows:
            query = 'SELECT * FROM {} WHERE row_date = {};'.format
            query=query(self.symbol,date)

        self._dfFromBase=pd.read_sql_query(query, con,index_col="Time")
        con.close()
        if dt:
            self._dfFromBase.index=pd.to_datetime(self._dfFromBase.index)
        return self._dfFromBase

    def to_sqlbase(self):
        con = sqlite3.connect(self.base)
        self._dfToBase=self.get(format='frame',dt=False)
        if self.last_time_InBase[0:10]!=self.last_time[0:10]:
            print('!new data company: ',self.symbol,'has been added')
            self.last_time_InBase=self.last_time
            self._dfToBase.to_sql(self.symbol,con=con,if_exists='append',index_label='Time')
        else:
            print('!there arent new data company: ',self.symbol)
        con.close()

    def drop_all(self):
        con  = sqlite3.connect(self.base)
        cursor = con.cursor()
        dropDataFrame = "DROP TABLE {}".format
        try:
            cursor.execute(dropDataFrame(self.symbol))
            self.reset_lastDate()
        except:
            pass
        con.close()

#------------------- READ BASE ---------------------------------------#
class readBase:
    def __init__(self,labels):
        self.labels=labels
    def get(self):
        self._df={}
        self.notInBase=[]
        for key in self.labels:
            try: 
                self._df[key]=DataAV(symbol=key).from_sqlbase()
            except:
                self.notInBase.append(key)
        return self._df

#-----------------------SAVE BASE-----------------------------------------#

class saveBase:
    def __init__(self,labels):
        self.labels=labels

    def save(self):
       self.not_exist=[]
       for key in self.labels:
           for i in np.arange(3):
               try:
                   DataAV(symbol=key).to_sqlbase()
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
