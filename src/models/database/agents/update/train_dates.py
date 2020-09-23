from src.models.database.agents.agents import DataBaseOneAgent
from src.models.database.update import UpdateValidFieldsDocumentDB
import pandas as pd

class UpdateAgentTrainDates(DataBaseOneAgent, UpdateValidFieldsDocumentDB):

    _valid_fields = ('init_train_date', 'end_train_date')
    def __init__(self, stock_name):
        super().__init__(stock_name=stock_name)

    @property
    def valid_fields(self):
        return self._valid_fields

    def update_init_date(self, where, init_date, **kwargs):
        return self.update_one(where, 
                                self._dict_field_date(0, init_date),
                                 **kwargs)

    def update_many_init_date(self, where, init_date, **kwargs):
        return self.update_many(where, 
                                self._dict_field_date(0, init_date),
                                 **kwargs)

    def updatey_end_date(self, where, end_date, **kwargs):
        return self.update_one(where, 
                               self._dict_field_date(1, end_date),
                               **kwargs)

    def update_many_end_date(self, where, end_date, **kwargs):
        return self.update_many(where, 
                                self._dict_field_date(1, end_date),
                                 **kwargs)

    def update_dates(self, where, init_date, end_date, **kwargs):
        return self.update_one(where, 
                               self._dict_fields_dates(init_date, end_date),
                                **kwargs)

    def update_many_dates(self, where, init_date, end_date, **kwargs):
        return self.update_many(where, 
                                self._dict_fields_dates(init_date, end_date),
                                 **kwargs)

    def _dict_field_date(self, field, date):
        return {self._valid_fields[field] : self._datetime(date)}

    def _dict_fields_dates(self,  init_date, end_date):
        return dict(
                    zip(map(self._datetime, 
                            (init_date, end_date)),
                        self._valid_fields
                        )
                    )
                    
    @staticmethod
    def _datetime(date):
        return pd.to_datetime(date) if not isinstance(date, pd.Timestamp) else date
