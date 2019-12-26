import Reader as rd
import unittest
########################################################################################
         

 
class TestCompanyReader(unittest.TestCase):
    def setUp(self):
        self.reader=rd.Reader(3,60)
        self.list_dict=[{'function':'TIME_SERIES_INTRADAY',
            'symbol':'TWTR',
            'interval':'1min',
            'outputsize':'full',
            'datatype':'json',
            'apikey':'O39L8VIVYYJYUN3P'},

            {'function':'TIME_SERIES_INTRADAY',
            'symbol':'AAPL',
            'interval':'1min',
            'outputsize':'full',
            'datatype':'json',
            'apikey':'O39L8VIVYYJYUN3P'}]

    def test_list_json_valid(self):
        self.assertTrue(self.reader.read(self.list_dict))

    def test_companies_list_empty(self):
        ''' Description: Check return of empty list'''

        self.assertEqual(self.reader.read([]),
                         [{'Error':{'Error empty': 'empty list has been passed'}}])

    def test_list_json_invalid_keys(self):
        ''' Description: Check invalid keys in dict of the list'''

        self.assertEqual(self.reader.read( [{'function':'TIME_SERIES_INTRADAY',
                                             'smbol':'AAPL', #
                                            'interval':'1min',
                                            'outputsize':'full',
                                            'datatype':'json',
                                            'apikey':'O39L8VIVYYJYUN3P'}] ),

                                            [{'Error': {'Error keys': 'Missing or Invalid keys'}}])

    def test_not_strings(self):
        
        self.assertEqual(self.reader.read( [{'function':'TIME_SERIES_INTRADAY',
                                             'symbol':10, #
                                            'interval':'1min',
                                            'outputsize':'full',
                                            'datatype':'json',
                                            'apikey':'O39L8VIVYYJYUN3P'}] ),

                                            [{'Error':{'Error String': 'Any value is not str'}}])

    def test_all_errors(self):
        self.assertCountEqual(self.reader.read( [{'function':'TIME_SERIES_INTRADAY',
                                                  'symbol':10, #
                                                  'interval':'1min',
                                                  'outputsize':'full',
                                                  'datatype':'json',
                                                  'apikey':'O39L8VIVYYJYUN3P'},
                                                {'function':'TIME_SERIES_INTRADAY',
                                                  'sybol':'AAPL', #
                                                  'interval':'1min',
                                                  'outputsize':'full',
                                                  'datatype':'json',
                                                  'apikey':'O39L8VIVYYJYUN3P'}
                                                  ] ),
                                                  [{'Error':{'Error String': 'Any value is not str'}},
                                                   {'Error': {'Error keys': 'Missing or Invalid keys'}}])

    
        
if __name__ == '__main__':
    unittest.main()