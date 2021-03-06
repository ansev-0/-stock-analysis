from src.train.orders.database.agents.agents import DataBaseOneAgent

class FindTrainAgent(DataBaseOneAgent):

    def find_many(self, where, **kwargs):
        return self.collection.find(where, **kwargs)

    def find_one(self, where, **kwargs):
        return self.collection.find_one(where, **kwargs)

    def find_by_status(self, status, **kwargs):
        return self.find_many({'status' : status}, **kwargs)


    def find_by_train_id(self, train_id, **kwargs):
        return self.find_one({'_id' : train_id},
                             **kwargs)
