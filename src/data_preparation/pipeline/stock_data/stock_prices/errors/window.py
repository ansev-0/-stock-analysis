
from src.exceptions.data_preparation_exceptions import PipelineError

class CheckErrors:
    def __init__(self, window_class):
        self.window_class = window_class
    
    def function_implemented(self, function):
        if not hasattr(self.window_class, function):
            raise PipelineError(f'Not Implemented {function} in class {self.window_class}' ,
                                ValueError)