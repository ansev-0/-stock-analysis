from src.acquisition.alphavantage import reader
import unittest
class Test_reader(unittest.TestCase):
    def setUp(self):
        self.time_series_intraday={'function':'TIME_SERIES_INTRADAY',
           'symbol':'TWTR',
           'interval':'1min',
           'outputsize':'full',
           'datatype':'json',
           'apikey':'O39L8VIVYYJYUN3P'}

        self.time_series_daily={'function':'TIME_SERIES_DAILY',
           'symbol':'TWTR',
           'outputsize':'compact',
           'datatype':'json',
           'apikey':'O39L8VIVYYJYUN3P'}


        self.time_series_daily_adjusted={'function':'TIME_SERIES_DAILY_ADJUSTED',
           'symbol':'TWTR',
           'outputsize':'compact',
           'datatype':'json',
           'apikey':'O39L8VIVYYJYUN3P'}


        self.time_series_weekly={'function':'TIME_SERIES_WEEKLY',
           'symbol':'TWTR',
           'outputsize':'compact',
           'datatype':'json',
           'apikey':'O39L8VIVYYJYUN3P'}


        self.time_series_weekly_adjusted={'function':'TIME_SERIES_WEEKLY_ADJUSTED',
           'symbol':'TWTR',
           'outputsize':'compact',
           'datatype':'json',
           'apikey':'O39L8VIVYYJYUN3P'}

        self.reader=reader.ReaderAlphaVantage(params = {'apikey':'O39L8VIVYYJYUN3P'})

    def test_correct_requests(self):
        valid, errors = self.reader.read(queries=[self.time_series_intraday,
        self.time_series_daily,
        self.time_series_daily_adjusted,
        self.time_series_weekly,
        self.time_series_weekly_adjusted],frame = True,keys_response = ['symbol','function'],enumerate_axis = True)
        self.assertFalse(errors)

if __name__ == '__main__':
    unittest.main()