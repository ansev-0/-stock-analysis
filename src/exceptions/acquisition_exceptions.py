from src.exceptions import new_exception

class AlphaVantageError(new_exception.NewException):
    pass

class Last10kError(new_exception.NewException):
    pass