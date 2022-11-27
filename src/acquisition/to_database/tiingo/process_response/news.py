from src.acquisition.to_database.tiingo.process_response.process_response import ProcessResponse
import re
import pandas as pd
from functools import reduce

class ProcessResponseNews:

    DATES_FIELDS = ('crawl_date', 'published_date')

    def rename_fields(self, json_in):
        return {re.sub(r'(?<=[a-z])[A-Z]|[A-Z](?=[^A-Z])', r'_\g<0>', 
                       field)
                  .lower()
                  .strip('_') : value 
                for field, value in json_in.items()}
        

    def change_type_fields(self, json_in):
        for field in self.DATES_FIELDS:
            json_in[field] = pd.to_datetime(json_in[field])
        json_in['id'] = str(json_in['id'])
        
        return json_in

    def build_struct_to_db(self, json_in):
        data_struct = {key : value for key, value in json_in.items() if key != 'id'}
        return {'_id' : pd.to_datetime(json_in['published_date'].date()), 
                json_in['id'] : data_struct}

    def __call__(self, json_in):
        return [reduce(lambda result, func: func(result), 
                      (self.rename_fields, self.change_type_fields, self.build_struct_to_db), 
                      dict_) for dict_ in json_in]

    def filter_fields(self):
        pass

    def mapper_fields(self):
        pass