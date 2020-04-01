from src.database.database import DataBase

class AcquisitionIncidents:
    def __init__(self):
        self.__database = DataBase()
        self.__database.connect('acquisition_incidents')
        

    
    def report(self, api, query, error_returned):
        return self.__database.database[api].update_one({'query' : query},
                                                        {'$set': {'return' : error_returned}},
                                                        upsert=True)
    
    def delete_incident(self, api, query):
        return self.__database.database[api].delete_one({'query' : query})
        
    def delete_all_incidents(self, api):
        return self.__database.database[api].delete_many({})

    def get_incident(self, api, query):
        return self.__database.database[api].find_one({'query' : query})

    def get_all_incidents(self, api):
        return list(self.__database.database[api].find({}))

