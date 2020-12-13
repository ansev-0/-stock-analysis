from src.data_preparation.database.database import DataPreparationDataBase
import pandas as pd



class EmbeddingDimensionDataBase(DataPreparationDataBase):
    _collection = 'embedding_dimension'

    def __init__(self):
        super().__init__()
        self._collection_connection = self._database.database[self.collection_name]

    def update_one(self, dict_data):

        if self._input_has_correct_format(dict_data):
            # convert to datetime 
            for key in ('start', 'end'):
                if not isinstance(dict_data[key], pd.Timestamp):
                    dict_data[key] = pd.to_datetime(dict_data[key])
            #update
            out = self._collection_connection.update_one({'company' : dict_data['company'], 
                                                          'start' : dict_data['start'], 
                                                          'end' : dict_data['end'],
                                                          'frecuency' :dict_data['end']},
                                                         {'$set' : dict_data}, 
                                                         upsert=True)
            return out

        else:
            raise ValueError('Invalid keys, You must pass: company, frecuency, start, end and value fields')



    def find_one(self, dict_data):

        if self._query_has_correct_format(dict_data):
            # convert to datetime 
            for key in ('start', 'end'):
                if not isinstance(dict_data[key], pd.Timestamp):
                    dict_data[key] = pd.to_datetime(dict_data[key])
            #find
            out = self._collection_connection.find_one(dict_data, 
                                                       projection = {'value' : 1, '_id' : 0})
            try:
                return out['value']
            except:
                return None
        else:
            raise ValueError('Invalid keys, You must pass: company, start and end fields')




    @staticmethod
    def _input_has_correct_format(input_dict):
        return tuple(sorted(input_dict.keys())) == ('company', 'end', 'frecuency', 'start', 'value')


    @staticmethod
    def _query_has_correct_format(query_dict):
        return tuple(sorted(query_dict.keys())) == ('company', 'end', 'frecuency', 'start')

