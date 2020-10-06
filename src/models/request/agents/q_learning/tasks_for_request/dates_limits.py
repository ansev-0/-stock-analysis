from src.models.database.dates import DatetimeDates
from src.models.database.agents.fields import limits_data_train, limits_data_val
from src.tools.reduce_tools import flatten_adding


class DatesLimitsTask:

    def __call__(self, limits_train, limits_val=None):
        return self._get_dates_dict(limits_train, limits_val)

    def _get_dates_dict(self, limits_train, limits_val):

        if limits_val is not None:
            return DatetimeDates()\
                .dates_for_save_from_tuples(flatten_adding((limits_data_train,
                                                            limits_data_val)),
                                            flatten_adding((limits_train, limits_val))
                                                    
        )
        return DatetimeDates().dates_for_save_from_tuples(limits_data_train,
                                                          limits_train)
                                                          