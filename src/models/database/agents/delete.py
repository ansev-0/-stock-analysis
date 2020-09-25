from src.models.database.agents.agents import DataBaseOneAgent

class DeleteTrainAgent(DataBaseOneAgent):

    def delete_many(self, where):
        return self.collection.delete_many(where)

    def delete_one(self, where):
        return self.collection.delete_one(where)

    def delete_on_status(self, status):
        return self.delete_many({'status' : status})

    def delete_on_type_model(self, type_model):
        return self.delete_many({'type_model' : type_model})

    def delete_on_type_and_id_model(self, type_model, type_id):
        return self.delete_one({'type_model' : type_model,
                                'type_id' : type_id})
