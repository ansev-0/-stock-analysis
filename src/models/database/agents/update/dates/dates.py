from src.models.database.agents.agents import DataBaseOneAgent
from src.models.database.update import UpdateValidFieldsDocumentDB
import pandas as pd
from tools.filter import filter_dict

class UpdateAgentDates(DataBaseOneAgent, UpdateValidFieldsDocumentDB):

    _valid_fields = []

    @property
    def valid_fields(self):
        return self._valid_fields


    def _update_dict(self, data):
        return {'$set' : {key : self.datetime(value) 
                          for key, value in data.items()
                          if key in self.valid_fields}}

    @staticmethod
    def datetime(date):
        return pd.to_datetime(date) if not isinstance(date, pd.Timestamp) else date


class UpdateAgentInitEndDates(UpdateAgentDates):

    def update_init(self, where, init, **kwargs):
        return self.update_one(where, self._dict_date(0, init), **kwargs)

    def update_many_init(self, where, init, **kwargs):
        return self.update_many(where, self._dict_date(0, init), **kwargs)

    def update_end(self, where, end, **kwargs):
        return self.update_one(where, self._dict_date(1, end), **kwargs)

    def update_many_end(self, where, end, **kwargs):
        return self.update_many(where, self._dict_date(1, end), **kwargs)

    def update_dates(self, where, init, end, **kwargs):
        return self.update_one(where, self._dict_dates((init, end)), **kwargs)

    def update_many_dates(self, where, init, end, **kwargs):
        return self.update_many(where, self._dict_dates((init, end)), **kwargs)

    def _dict_date(self, index, date):
        return {self._valid_fields[index] : date}

    def _dict_dates(self, dates):
        return dict(zip(self._valid_fields, dates))




