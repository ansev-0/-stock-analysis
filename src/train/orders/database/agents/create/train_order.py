from src.train.orders.database.agents.agents import DataBaseOneAgent
from src.tools.reduce_tools import combine_dicts

class CreateTrainOrderAgent(DataBaseOneAgent):

    def __call__(self,  **kwargs):
        return self.collection.insert_one(combine_dicts(kwargs, {'status' : 'pending'}))
