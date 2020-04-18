from src.exceptions.data_preparation_exceptions import PipelineError

class CheckErrors:

    def function_implemented(self, dataframe, function):
        if not hasattr(dataframe, function):
            raise PipelineError(f'Not Implemented {function} in class {self.window_class}' ,
                                ValueError)

    def correct_columns(self, dataframe):
        if not (sorted(list(map(lambda label: label.lower(),
                                dataframe.columns))) == ['close', 'high', 'low', 'open']):
            raise PipelineError('DataFrame columns must be  open, high, low and close', ValueError)
            

