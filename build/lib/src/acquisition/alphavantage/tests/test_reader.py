from acquisition.alphavantage import reader
import unittest
print('hola')
class Test_reader(unittest.TestCase):
    def setUp(self):
        self.load_dict={'function':'TIME_SERIES_INTRADAY',
           'symbol':'TWTR',
           'interval':'1min',
           'outputsize':'full',
           'datatype':'json',
           'apikey':'O39L8VIVYYJYUN3P'}
        self.reader=reader.ReaderAlphaVantage()

    def test_correct_request(self):
        valid, errors = self.reader.read(queries=[self.load_dict]*5)
        #print(valid)
        self.assertFalse(errors)

if __name__ == '__main__':
    unittest.main()