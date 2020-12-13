from src.train.database.results.agents.agent import ResultTrainDataBase

class FindResultTrainDataBase(ResultTrainDataBase):

    def find_one(self, *args, **kwargs):
        return self.collection.find_one(*args, **kwargs)

    def find_many(self, *args, **kwargs):
        return self.collection.find(*args, **kwargs)

    def find_by_id(self, _id, **kwargs):
        return self.find_one({'_id' : _id}, **kwargs)

    def find_by_ids(self, _ids, **kwargs):
        return self.find_many({'_id' : {'$in' : _ids}})

    def find_by_source_data(self, source_data, **kwargs):
        return self.find_many({'source_data' : source_data}, **kwargs)