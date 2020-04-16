from src.data_preparation.pipeline.pipeline import Pipeline
from functools import wraps
from src.data_preparation.pipeline.stock_data.summary import SummaryStockData

class PipelineStockData(Pipeline):
    

    def __init__(self):
        self.summary = SummaryStockData()
        self._scalers = None
        self._data = None

    @property
    def data(self):
        return self._data

    @property
    def scalers(self):
        return self._scalers

    def _summary(self, **kwargs):
        self.summary.enter_params(**kwargs)
        self.summary.build()
        return self.summary.str_summary


    @classmethod
    def process(cls, function):

        @wraps(function)
        def process_data(self, return_summary=True, *args, **kwargs):
            (self._scalers, self._data,
             initial_index, final_index), additional_summary_information = function(self, *args, **kwargs)

            if not additional_summary_information:
                additional_summary_information = {}

            if return_summary:
                print(self._summary(priority = self.priority,
                                    initial_index=initial_index,
                                    final_index=final_index,
                                    scaler=self._scalers,
                                    transform_functions=function.__doc__,
                                    **additional_summary_information))
            return None

        return process_data


class B(PipelineStockData):
    pass

