import time
import requests
from src import request_api
from src.acquisition.errors_response import check_errors_alphavantage as errors_response
from src.acquisition.errors_queries import check_errors_alphavantage as error_queries
from src.acquisition.format_builders import alphavantage_formats
from src.exceptions.acquisition_exceptions import AlphaVantageError
from src.tools.builders import inlist, join_values_filtered_by_keys

class ReaderAlphaVantage():

    def __init__(self, delays=[60, 10], **kwards):

        self.format_builder = alphavantage_formats.FormatBuilderAlphavantage()
        self.config(delays)
        self.test_response = errors_response.ErrorsResponseApiAlphavantage()
        self.test_queries = error_queries.ErrorsQueryApiAlphavantage()
        self.request = request_api.RequestsApi(base_url='https://www.alphavantage.co/query',
                                               **kwards)

    def _get_transform_function(self, frame):
        if frame:
            return self.format_builder.build_frame
        return self.format_builder.get_data_dict

    def config(self, delays):
        '''
        This function configures the number of attempts
        as well as the intermediate waits.
        '''
        self.attemps = len(delays)+1
        self.delays = delays

    def read(self, queries, keys_response, frame=False, **kwards):

        '''
        This function returns two dictionaries.
        One of them with invalid answers (dict_errors)
         and the other with valid answers (dict_valids).
        The dictionary keys will be those specified in keys_response
        This function returns two dictionaries,


        Parameters
        ----------
        queries : tuple,list or dict
            API request, list or tuple of dictionaries or a dictionary.

        frame: bool
            True if the output format must be a DataFrame, otherwise it returns a dictionary
        '''

        list_queries = inlist(queries)
        format_output = self._get_transform_function(frame)
        dict_valids = {}
        dict_errors = {}

        for query in list_queries:

            # Getting key
            key_dict = join_values_filtered_by_keys(query, keys_response)
            self.test_queries.empty_keys(key_dict)
            # Trying get response
            count_attemps = 0
            while count_attemps < self.attemps:
                try:
                    response = self.request.get(params=query)
                    print(response.url)
                except requests.exceptions.RequestException as error:
                    dict_errors[key_dict] = [query, error, response.status_code]
                    count_attemps = self.attemps
                else:
                    json = response.json()
                    count_attemps += 1 #attemp n

                    try:
                        self.test_response.pass_test(json, query)

                    except AlphaVantageError:
                        if count_attemps == self.attemps:
                            #add error to dict_errors
                            dict_errors[key_dict] = [query, json.copy(), response.status_code]
                        else:
                            #try again
                            
                            time.sleep(self.delays[count_attemps-1])
                    else:
                        #connect succesfull, save useful data
                        dict_valids[key_dict] = format_output(json=json,
                                                              function=query['function'],
                                                              **kwards)
                        
                        break
        return dict_valids, dict_errors
