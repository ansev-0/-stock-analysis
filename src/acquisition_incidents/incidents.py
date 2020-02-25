from src.database.database import DataBase

class AcquisitionIncidents(DataBase):
    def __init__(self):
        super().__init__(name_database='acquisition_incidents')
        
    def report(self, api, query, error_returned):
        return self.database[api].update_one({'query' : query},
                                             {'$set': {'return' : error_returned}},
                                             upsert=True)
    
    def delete_incident(self, api, query):
        return self.database[api].delete_one({'query' : query})
        
    def delete_all_incidents(self, api):
        return self.database[api].delete_many({})

    def get_incident(self, api, query):
        return self.database[api].find_one({'query' : query})

