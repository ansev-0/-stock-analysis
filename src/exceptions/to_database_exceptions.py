from src.exceptions import new_exception

class ToDataBaseError(new_exception.NewException):
    pass

class ToDataBaseAlphaVantageError(new_exception.NewException):
    pass

class ToDataBaseLast10KError(new_exception.NewException):
    pass