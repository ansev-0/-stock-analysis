from src.models.database.agents.agents import DataBaseOneAgent
from src.models.database.update import UpdateValidFieldsDocumentDB

class UpdateAgentTrainStatus(DataBaseOneAgent, UpdateValidFieldsDocumentDB):

    _valid_fields = ('status', )
    _valids_status = ('pending', 'running', 'done', 'interrupt')

    def __init__(self, stock_name, status):
        super().__init__(stock_name=stock_name)
        self.status = status

    @property
    def valid_fields(self):
        return self._valid_fields

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._check_valid_status(status)
        self._status = status

    @property
    def dict_status(self):
        return {'status' : self._status}

    def set_one(self, where, **kwargs):
        self.update_one(where, self.dict_status, **kwargs)

    def set_many(self, where, **kwargs):
        self.update_many(where, self.dict_status, **kwargs)

    def set_on_id_and_type_model(self, id_type, type_model, **kwargs):
        return self.set_one({'type_model' : type_model , 'id_type' : id_type})

    def set_on_id(self, id, **kwargs):
        return self.set_one({'_id' : id}, **kwargs)

    def set_on_status(self, status, **kwargs):
        return self.set_many({'status' : status}, **kwargs)

    def _check_valid_status(self, status):
        if not status in self._valids_status:
            raise ValueError(f'You must pass a valid status: {self._valids_status}')
