import ReaderDataCompaniesDB as reader
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
class VolumeAnalizer(reader.ReaderCompany):



    def getData(self,companies,start_date= '2019-08-05 00:00:00', end_date=(datetime.now() + pd.Timedelta(weeks=5) ).strftime(format='%Y-%m-%d %H:%M:%S'),volume_data=True,all_data=False):
        df_list=[]
        self.all_data_dict={}
        for company in companies:
            df=self.read(company=company,start_date=start_date,end_date=end_date,df=True) 
            if isinstance(df,pd.DataFrame):
                df_list.append(df['volume'].rename(company))
                self.all_data_dict[company]=df

        df=pd.concat(df_list,axis=1)
        out=(df.describe().T,)
        if volume_data:
            out= out + (df,)

        if all_data:
            out=out + (self.all_data_dict,)

        return out
        

def initialize():
    return VolumeAnalizer()