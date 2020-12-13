from src.exceptions.readbase_exceptions import GetFromDataBaseError
class CheckErrorsDataFromDataBase:
    @staticmethod
    def check_format(format_output):
        if format_output not in ['dict', 'dataframe']:
            raise GetFromDataBaseError