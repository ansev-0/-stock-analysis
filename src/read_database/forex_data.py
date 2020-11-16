from src.read_database.reader import DataFromDataBase
from src.exceptions.readbase_exceptions import GetFromDataBaseError


class ForexDataFromDataBase(DataFromDataBase):
    '''
    This class is used for reading forex_data databases.
    
    '''

    def get(self, from_symbol, to_symbol, start, end, **kwargs):

        '''

        This function get forex data from pair (from_symbol, to_symbol) database between two dates:
        start and end (both inclusive).

        Parameters
        --------------
        from_symbol: label(name).
        to_symbol: label(name).
        start: str or pd.Timedelta.
        end str or pd.Timedelta.

        '''
        return super().get(f'{from_symbol}_TO_{to_symbol}', start, end, **kwargs)


    @classmethod
    def intraday_dataframe(cls, freq):
        return cls.__dataframe(db_name=f'forex_data_intraday_{freq}')

    @classmethod
    def daily_dataframe(cls):
        return cls.__dataframe(db_name='forex_data_daily')

    @classmethod
    def intraday_dict(cls, freq):
        return cls.__dict(db_name=f'forex_data_intraday_{freq}')

    @classmethod
    def daily_dict(cls):
        return cls.__dict(db_name='forex_data_daily')

    @classmethod
    def __dataframe(cls, **kwargs):
        return cls(format_output='dataframe', **kwargs)

    @classmethod
    def __dict(cls, **kwargs):
        return cls(format_output='dict', **kwargs)
