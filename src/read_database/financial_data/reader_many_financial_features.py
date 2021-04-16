from src.read_database.financial_data.reader_financial_data import FinancialDataFromDataBase
import pandas as pd

class ManyFinancialFeaturesFromDataBase:

    _DEFAULT_FEATURES = ('cash_flow', 'earnings', 
                         'balance_sheet', 'income_statement')

    _DEFAULT_FRECUENCIES = ('quarterly, anuual')

    def __init__(self, 
                 features=None, 
                 format_output='dataframe', 
                 frecuency='quarterly'):

        self._clients = None
        self._features = None
        self.format_output = format_output
        self.frecuency = frecuency
        self.features = features
        
        

    @property
    def clients(self):
        return self._clients

    @property
    def frecuency(self):
        return self._frecuency

    @frecuency.setter
    def frecuency(self, frecuency):
        self._frecuency = self._validate_frecuency(frecuency)


    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, features):
        self._features = self._validate_features(features) \
            if features is not None else self._DEFAULT_FEATURES
        
        self._clients = list(
            map(lambda feature: FinancialDataFromDataBase(db_name=f'{feature}_{self._frecuency}', 
                                                          format_output='dataframe'),
                self._features
               )
        )


    def get(self, collection, start, end, **kwargs):
        
        list_results = [data.add_prefix(f'{self._DEFAULT_FEATURES[i]}_') for i, data in 
                
                         enumerate(map(lambda client: client.get(collection, 
                                                                start, 
                                                                end, 
                                                                **kwargs),
                                        self._clients))
                        if isinstance(data, pd.DataFrame)]

        concat_df = pd.concat(list_results, axis=1, join='inner') if list_results else None

        if list_results is None:
            return None
        
        return concat_df if self.format_output == 'dataframe' else concat_df.to_dict(orient='index')


    def _validate_features(self, features):
        if features not in self._DEFAULT_FEATURES:
            raise ValueError('Invalid features')
        return features

    def _validate_frecuency(self, frecuency):
        if frecuency not in self._DEFAULT_FRECUENCIES:
            raise ValueError('Invalid frecuency')
        return frecuency


    
