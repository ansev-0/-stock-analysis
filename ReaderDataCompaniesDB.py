from pymongo import MongoClient
import pandas as pd
from datetime import datetime

class ReaderCompany:

    def __init__(self):
        self._client=MongoClient()

    #private method of instance
    def _CheckStringType(self,val):
        if not isinstance(val,str):
            raise TypeError(f'{val} must be string')

    #public method of instance
    def read(self,company,start_date,end_date,df=False,dt=True):

        data={}

        #Check type string
        self._CheckStringType(company)
        self._CheckStringType(start_date)
        self._CheckStringType(end_date)

        #Seelct start and end Date
        start_datetime=pd.to_datetime(start_date)
        end_datetime=pd.to_datetime(end_date)

        if start_datetime > end_datetime:
            raise ValueError('The initial date has to be before the final date')
        else:

            #Creating range of year to acces diferents DataBases
            for age_month in pd.date_range(start_date,end_date,freq='M').to_period('M'):

                # Creating connect db for this year
                db=self._client[f'AV{age_month.year}']
                #Access for data of the company and  month-year
                collection=db[company]
                try:
                   out=collection.find_one({'_id':str(age_month)})
                   if out is not None:
                       del out['_id']
                       data.update(out)
                    
                except Exception:
                    pass #by define

        if not data:
            data.update({'Error':'There are not data in this range of data'})
        else:

            data={k:v  for k,v in data.items() if start_datetime <= pd.to_datetime(k) <= end_datetime }
            if df:
                #convert to dataframe
                data=pd.DataFrame(data).T.astype(float)
                data.columns=data.columns.str[3:]
                if dt:  #only if df=True
                    data.index=pd.to_datetime(data.index)
                
        return data


def Reader():
    return ReaderCompany()

                    















