from pymongo import MongoClient
import datetime
class DBAV:
    def __init__(self):
        self._client=MongoClient()

    def _CheckStringType(self,val):
        if not isinstance(val,str):
            raise TypeError(f'{val} must be string')

    def push(self,data,collection,year=str(datetime.datetime.now().year)):
        self._CheckStringType(year)
        self._CheckStringType(collection)
        db=self._client[f'AV{year}']
        self._company=db[collection]
        self._company.update_one({'_id':data['_id']},{'$set':data},upsert=True)

    def _AV_companies(self,collection):
        self._CheckStringType(collection)
        db=self._client['AVcompanies']
        self._collection=db[collection]
    
    def get_companies(self,collection,filter,field):
        self._AV_companies(collection=collection)
        return self._collection.find_one(filter)[field]

    def update_companies(self,data,collection,filter,diagnostic=False):
        self._AV_companies(collection=collection)
        self._collection.update_one(filter,{'$set':data},upsert=True)


def DBaseAV():
    return DBAV()