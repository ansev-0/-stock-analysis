from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from functools import reduce

class MinMaxScalerFitTransform:

    def __init__(self, feature_range=(-1, 1)):
        self.feature_range = feature_range

    def array(self, array, transform=True):
        scaler = self._fit_scaler(array)
        if transform:
             array = scaler.transform(array)
        return scaler, array

    def dataframe(self, dataframe, **kwargs):
        scaler, array = self.array(dataframe, **kwargs)
        return scaler, pd.DataFrame(data=array, index=dataframe.index, columns=dataframe.columns)

    def series(self, serie, **kwargs):
        scaler, array = self.array(serie.values[:, None], **kwargs)
        return scaler, pd.Series(index = serie.index, name=serie.name, data=array.squeeze())

    def _fit_scaler(self, values):
        scaler = MinMaxScaler(feature_range=self.feature_range)
        scaler.fit(values)
        return scaler

class MinMaxScalerFitTransformMany(MinMaxScalerFitTransform):


    def tuple_array_flatten(self, tuple_array, transform=True):
        return reduce(lambda cum_tuple, new_tuple: cum_tuple + new_tuple,
                      self.__map(tuple_array, transform))

    def tuple_array(self, tuple_array, transform=True):
        return tuple(self.__map(tuple_array, transform))

    def dict_array(self, dict_array, transform=True):
        return dict(zip(dict_array.keys(),
                        self.__map(dict_array.values(), transform)))

    def __map(self, tuple_array, transform):
        return map(*self.__map_args(tuple_array, transform))

    def __map_args(self, tuple_array, transform):
        if isinstance(transform, bool):
                return lambda tup: self.array(tup, transform), tuple_array
        return lambda tup: self.array(*tup),  zip(tuple_array, transform)



class MinMaxScalerFitTransformWithMargins(MinMaxScalerFitTransform):
    
    def array_with_margins(self, array, percentage):
        array_to_scale = np.vstack([array,
                                    (np.max(array, axis=0)*(1+percentage)),
                                    (np.min(array,axis=0)*(1-percentage))])
        
        scaler, array = self.array(array_to_scale)
        return scaler, array[:-2,:]
    
    def dataframe_with_margins(self, dataframe, percentage, **kwargs):
        scaler, array = self.array_with_margins(dataframe, percentage, **kwargs)
        return scaler, pd.DataFrame(data=array, index=dataframe.index, columns=dataframe.columns)

    def series_with_margins(self, serie, percentage, **kwargs):
        scaler, array = self.array_with_margins(serie.values[:, None], percentage, **kwargs)
        print(array)
        return scaler, pd.Series(index = serie.index, name=serie.name, data=array.squeeze())



