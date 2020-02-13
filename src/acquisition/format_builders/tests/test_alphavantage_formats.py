#Libraries
import os
import sys
import unittest
from unittest.mock import MagicMock
import pandas as pd
from src.acquisition.format_builders import alphavantage_formats
from src.tools.builders import inlist
from src.tools import interface_json_files

#Current path
SCRIPT_PATH = os.path.realpath(os.path.dirname(sys.argv[0]))

class CheckDataFrame(unittest.TestCase):
    def setUp(self):
        self.dataframe = pd.DataFrame()

    def check_columns(self, expected_columns):
        self.assertCountEqual(expected_columns, self.dataframe.columns.tolist())
    def check_index_type(self, expected_type):
        self.assertTrue(isinstance(self.dataframe.index, expected_type)) 
    def check_value_in_index(self, value, is_in):
        if is_in:
            self.assertTrue(value in self.dataframe.index)
        else:
            self.assertTrue(value not in self.dataframe.index) 
    def check_data_type(self, expected_types):
        expected_types = inlist(expected_types)
        data_types = [str(typ) for typ in self.dataframe.dtypes]
        self.assertCountEqual(expected_types, data_types)
    def check_ascending_index(self, ascending):
        index_serie = self.dataframe.index.to_series()
        self.assertTrue(index_serie.equals(index_serie.sort_values(ascending=ascending)))


class TestAlphavantageFormatsBuildFrame(CheckDataFrame):
    def setUp(self):
        mock = MagicMock(return_value=interface_json_files
                         .JsonResponseFiles(path=SCRIPT_PATH + '/json_files/')
                         .read('test_formats_json.json'))
        #Getting json
        self.json_dict = mock()
        #Creating object to test.
        self.builder_formats = alphavantage_formats.FormatBuilderAlphavantage()

    def test_timeseries_intraday(self):
        default_query = {'json' : self.json_dict['TIME_SERIES_INTRADAY'],
                         'function' : 'TIME_SERIES_INTRADAY'}
        #test default query
        self.dataframe = self.builder_formats.build_frame(**default_query)
        self.check_columns(['open', 'high', 'low', 'close', 'volume'])
        self.check_index_type(pd.DatetimeIndex)
        self.check_data_type(['float64']*5)
        self.check_ascending_index(ascending=True)
        #test with enumerate_axis = True
        self.dataframe = self.builder_formats.build_frame(**dict(default_query,
                                                                 **{'enumerate_axis':True}))
        self.check_columns(['1. open', '2. high', '3. low', '4. close', '5. volume'])
        #test with ascending = False
        self.dataframe = self.builder_formats.build_frame(**dict(default_query,
                                                                 **{'ascending':False}))
        self.check_ascending_index(ascending=False)
        #test with pd.to_datetime = False
        self.dataframe = self.builder_formats.build_frame(**dict(default_query,
                                                                 **{'to_datetime':False}))
        self.check_index_type(object)
        #Test with datatype = str
        self.dataframe = self.builder_formats.build_frame(**dict(default_query, **{'datatype':str}))
        self.check_data_type(['object']*5)

if __name__ == '__main__':
    unittest.main()
