from src.models.database.agents.agents import DataBaseOneAgent

class FindTrainAgent(DataBaseOneAgent):

    def find_many(self, where, **kwargs):
        return self.collection.find_many(where, **kwargs)

    def find_one(self, where, **kwargs):
        return self.collection.find_one(where, **kwargs)

    def find_by_status(self, status, **kwargs):
        return self.find_many({'status' : status}, **kwargs)

    def find_by_type_model(self, type_model, **kwargs):
        return self.find_many({'type_model' : type_model}, **kwargs)

    def find_by_type_and_id_model(self, type_model, id, **kwargs):
        return self.find_one({'type_model' : type_model,
                                '_id' : id},
                            **kwargs)
