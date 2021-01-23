from src.train.orders.request.agents.q_learning.tasks_for_request.\
    financial_data.get_data import GetDataTask
from src.train.orders.request.agents.q_learning.tasks_for_request.data_task import DataTask

class FinancialDataTask(DataTask):

    features = ('all', )
    data_from_db = GetDataTask()

    def __call__(self, symbol, *indexes):

        return tuple(
            map(lambda index : self._to_cache(self.data_from_db(symbol, index),
                              is_financial=True), indexes)
        )
            
