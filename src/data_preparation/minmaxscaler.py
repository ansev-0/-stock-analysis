from sklearn.preprocessing import MinMaxScaler
from functools import reduce

class MinMaxScalerFitTransform:

    def __init__(self, feature_range):
        self.feature_range = feature_range

    def array(self, array, transform=True):
        scaler = self._fit_scaler(array)
        if transform:
             array = scaler.transform(array)
        return scaler, array

    def _fit_scaler(self, values):
        scaler = MinMaxScaler(feature_range=self.feature_range)
        scaler.fit(values)
        return scaler

class MinMaxScalerFitTransformMany(MinMaxScalerFitTransform):


    def tuple_array(self, tuple_array, transform=True, flatten=True):
        mapper = map(*self.__map_args(tuple_array, transform))
        if flatten: 
            return reduce(lambda cum_tuple, new_tuple: cum_tuple + new_tuple, mapper)
        return tuple(mapper)



    def __map_args(self, tuple_array, transform):
        if isinstance(transform, bool):
                return lambda tup: self.array(tup, transform), tuple_array
        return lambda tup: self.array(*tup),  zip(tuple_array, transform)



