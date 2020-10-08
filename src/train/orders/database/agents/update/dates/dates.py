from src.models.database.agents.agents import DataBaseOneAgent
from src.models.database.update import UpdateValidFieldsDocumentDB
import pandas as pd
from tools.filter import filter_dict


class UpdateAgentInitEndDates(DataBaseOneAgent, UpdateValidFieldsDocumentDB):

    _valid_fields = []

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




