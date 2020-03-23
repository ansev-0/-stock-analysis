from sklearn.preprocessing import MinMaxScaler

class MinMaxScalerFitTransform:
    def array(self, array, feature_range=(-1, 1), transform=True):
        scaler = self._fit_scaler(array, feature_range=feature_range)
        if transform:
             array = scaler.transform(array)
        return scaler, array

    def dict_arrays(self, dict_array, feature_range=(-1, 1),  transform=None):
        if not transform:
            transform = list(dict_array)

        for key, array in dict_array.items():
            dict_array[key] = dict(zip(('scaler', 'values'),
                                       self.array(array,
                                                  feature_range=feature_range,
                                                  transform=key in transform)))    
        return dict_array

    def _fit_scaler(self, values, feature_range=(-1, 1)):
        scaler = MinMaxScaler(feature_range=feature_range)
        scaler.fit(values)
        return scaler