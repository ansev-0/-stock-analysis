from src.train.orders.database.agents.agents import DataBaseOneAgent
from src.database.update import UpdateValidFieldsDocumentDB
from datetime import datetime

class UpdateStartEndAgentTrain(DataBaseOneAgent, UpdateValidFieldsDocumentDB):

    _valid_fields = ('start_date_train', 'end_date_train')

    @property
    def valid_fields(self):
        return self._valid_fields


    def __call__(self, field, train_id):
        return self.update_one(where={'_id' : train_id}, data={field : datetime.now()})
