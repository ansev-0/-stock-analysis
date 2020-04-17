from src.data_preparation.pipeline.pipeline import Pipeline
from functools import wraps
from src.data_preparation.pipeline.stock_data.summary import SummaryStockData

class PipelineStockData(Pipeline):
    
    def __init__(self):
        self.summary = SummaryStockData()
        self._scalers = None
        self._data = None

    @classmethod
    def process(cls, function):

        @wraps(function)
        def process_data(self, show_summary=True, dict_summary=True, *args, **kwargs):

            data, additional_summary_information = function(self, *args, **kwargs)

            if len(data) == 3:
                self._scalers, self._data, initial_index = data
                final_index = initial_index
            else:
                self._scalers, self._data, initial_index, final_index = data

            if not additional_summary_information:
                additional_summary_information = {}

            return self._summary_management(show_summary, dict_summary)\
                (show_summary, dict_summary,
                 priority = self.priority,
                 initial_index=initial_index,
                 final_index=final_index,
                 scaler=self._scalers,
                 transform_functions=function.__doc__,
                 **additional_summary_information)

        return process_data

    @property
    def data(self):
        return self._data

    @property
    def scalers(self):
        return self._scalers

    def _write_summary(self, **kwargs):
        self.summary.enter_params(**kwargs)
        self.summary.build()

    def _summary_management(self, show_summary, dict_summary):

        if show_summary or dict_summary:
            return self._summary_actions
        return lambda *args, **kwargs: None

    def _summary_actions(self, show_summary, dict_summary, **kwargs):

        self._write_summary(**kwargs)
        if show_summary:
            print(self.summary.str_summary)
        if dict_summary:
            return self.summary.registry
        return None




            

        


