from src.exceptions import new_exception

class ScalerInputOutputError(new_exception.NewException):
    pass

class PipelineError(new_exception.NewException):
    pass