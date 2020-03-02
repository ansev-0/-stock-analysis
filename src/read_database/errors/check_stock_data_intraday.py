from src.exceptions.readbase_exceptions import GetFromDataBaseError
class CheckErrorsGetStockDataIntraday1minFromDataBase:
    @staticmethod
    def check_format(format_output):
        if format_output not in ['dict', 'dataframe']:
            raise GetFromDataBaseError