from APIalphavantage import AV
import DBAV
import numpy as np
import pymongo
import pandas as pd
import datetime


class AVacquisition:

    
    def __init__(self):
        self._DB=DBAV.DBaseAV()
        self._AVreader=AV.Interface()
        self._systemerror=False
        self._errorconnect=False
        self._reset_list_to_del()
        self._reset_dict_errors()


#private method of instance

    def reset_list_response(self):
        self.response=[]

    def _reset_list_to_del(self):
        self._list_to_del=[]

    def _reset_dict_errors(self):
        self.dict_errors={}

    def _Update_dict_errors(self,dict_to_update):
        self.dict_errors.update(dict_to_update)



    def _UpdateAfterError(self,key,value,errorconnect=False):

        if not errorconnect:
            #notify exceptional error
            self._systemerror=True
        else:
            #Notify error connect
            self._errorconnect=True

        self._Update_dict_errors({key:value})

        self._list_to_del.append(key)





    

    def _DiagnosticResponse(self):
        
        if isinstance(self.response,dict):

            for key,value in self.response.items():
                if 'Error connect' in value.keys():
                    self._UpdateAfterError(key,value,errorconnect=True)
                elif 'Error keys' in value.keys():
                    self._UpdateAfterError(key,value)
                    print({'System Error': {'Reader.py','Error Keys'}})
                    
                elif 'Error empty' in value.keys():
                    self._UpdateAfterError(key,value)
                    print({'System Error': {'Reader.py','Error empty'}})


        else:
            #action to do
            self._systemerror=True
            print({'System Error': {'Reader.py','Error empty, it could be cause by Builder.py'}})

        #delate error of the response to save in the database
        for key in self._list_to_del:
            del self.response[key]
        self._reset_list_to_del()



    def _readCompanies(self):
        self.response=self._AVreader.read(data=self.list_companies,frecuency=False,df=False,dt=False,container='dict')

    def _SaveInBase(self):

        for company,data in self.response.items():
            first_date=next(iter(data))
            year_id=first_date[0:4]
            month_year_API=first_date[0:7]
            data_with_id={'_id':month_year_API}
            data_with_id.update(data.copy())
            self._DB.push(data=data_with_id,collection=company,year=year_id)


#public method of instance

    def update_companies(self,collection,filter,field='valid_companies'):
        self.list_companies=self._DB.get_companies(collection=collection,filter=filter,field=field)
        #print(self.list_companies)

    def run(self):
        self._readCompanies()
        self._DiagnosticResponse()
        self._SaveInBase()
        if self._systemerror:
            raise RuntimeError('Exceptional error has ocurred, broken code')
        elif self._errorconnect:
            raise ValueError('Error connect: there are any company that has been added companies_errorconnect, execute: runErrors')   


def  take():
    return AVacquisition()