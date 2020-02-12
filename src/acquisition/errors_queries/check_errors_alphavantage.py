from src.exceptions.acquisition_exceptions import AlphaVantageError
from src.acquisition.errors_queries import check_errors
class ErrorsQueryApiAlphavantage(check_errors.ErrorsQueriesApi):
    def empty_keys(self, keys_response):
        if keys_response == '':
            raise AlphaVantageError('keys do not match the keys of the query', ValueError)