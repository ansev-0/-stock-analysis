from src.read_database.reader import ReaderDataBase
from src.tools.reduce_tools import combine_dicts
import pandas as pd

class FinancialDataFromDataBase(ReaderDataBase):
    '''
    This class is used for reading time series databases.
    '''
    


    def __init__(self, db_name, format_output='dataframe'):
        super().__init__(db_name, format_output)

    def get(self, collection, start, end, **kwargs):

        '''

        This function get data data from data data base between two dates:
        start and end (both inclusive).

        Parameters
        --------------
        collection: label(name)
        start: str or pd.Timedelta.
        end str or pd.Timedelta.

        '''
        dict_data = self._get_dict_from_database(collection,
                                                 start=self.__get_datetime_index(start),
                                                 end=self.__get_datetime_index(end),
                                                )
        if dict_data:
            dataframe = (
                self._build_dataframe(dict_data=dict_data, start=start, end=end, **kwargs))
            return self.func_transform_dataframe(dataframe=dataframe, **kwargs)
        return dict_data

        
    def _get_dict_from_database(self, data, start, end, **kwargs):
        consult_result = list(super()._get_dict_from_database(data, start, end, **kwargs))
        
        try:
            return combine_dicts(*({d['_id'].strftime(format='%Y-%m-%d %H:%M:%S') : {key : value 
                                                                                     for key, value in d.items() 
                                                                                     if key != '_id'}} 
                                   for d in super()._get_dict_from_database(data, start, end, **kwargs)))

        except TypeError as error:
            return None

    def _build_dataframe(self, dict_data, start, end, format_index=None, **kwargs):
        return self._builder_dataframe.build_dataframe_from_financial_timeseries_dict(dataframe=dict_data,
                                                                                      datetime_index=True,
                                                                                      format_index=format_index,
                                                                                      ascending=True).loc[start:end]  

    @staticmethod
    def __get_datetime_index(value):
        if isinstance(value, str):
            return pd.to_datetime(value)
        return value


    @classmethod
    def income_statement_quarterly_dataframe(cls):
        return cls._dataframe(db_name='income_statement_quarterly')

    @classmethod
    def income_statement_annual_dict(cls):
        return cls._dict(db_name='income_statement_annual')

    @classmethod
    def income_statement_quarterly_dict(cls):
        return cls._dict(db_name='income_statement_quarterly')

    @classmethod
    def income_statement_annual_dataframe(cls):
        return cls._dataframe(db_name='income_statement_annual')


    @classmethod
    def balance_sheet_quarterly_dataframe(cls):
        return cls._dataframe(db_name='balance_sheet_quarterly')

    @classmethod
    def balance_sheet_annual_dict(cls):
        return cls._dict(db_name='balance_sheet_annual')

    @classmethod
    def balance_sheet_quarterly_dict(cls):
        return cls._dict(db_name='balance_sheet_quarterly')

    @classmethod
    def balance_sheet_annual_dataframe(cls):
        return cls._dataframe(db_name='balance_sheet_annual')

    @classmethod
    def cash_flow_quarterly_dataframe(cls):
        return cls._dataframe(db_name='cash_flow_quarterly')

    @classmethod
    def cash_flow_annual_dict(cls):
        return cls._dict(db_name='cash_flow_annual')

    @classmethod
    def cash_flow_quarterly_dict(cls):
        return cls._dict(db_name='cash_flow_quarterly')

    @classmethod
    def cash_flow_annual_dataframe(cls):
        return cls._dataframe(db_name='cash_flow_annual')

    @classmethod
    def earnings_quarterly_dataframe(cls):
        return cls._dataframe(db_name='earnings_quarterly')

    @classmethod
    def earnings_annual_dict(cls):
        return cls._dict(db_name='earnings_annual')

    @classmethod
    def earnings_quarterly_dict(cls):
        return cls._dict(db_name='earnings_quarterly')

    @classmethod
    def earnings_annual_dataframe(cls):
        return cls._dataframe(db_name='earnings_annual')


    @classmethod
    def stock_overview_quarterly_dataframe(cls):
        return cls._dataframe(db_name='stock_overview_quarterly')

    @classmethod
    def stock_overview_annual_dict(cls):
        return cls._dict(db_name='stock_overview_annual')

    @classmethod
    def stock_overview_quarterly_dict(cls):
        return cls._dict(db_name='stock_overview_quarterly')

    @classmethod
    def stock_overview_annual_dataframe(cls):
        return cls._dataframe(db_name='stock_overview_annual')

