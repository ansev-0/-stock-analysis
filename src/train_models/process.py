from src.data_preparation.minmaxscaler import MinMaxScalerFitTransformMany
import numpy as np

class GetCurrenDataSetScaled():
    def __init__(self, array, feature_range = (-1,1)):
        self.array = array
        (self.scaler, self.values_scaler) = (MinMaxScalerFitTransformMany(feature_range)
                                             .array(array))

    def update_current_dataset(self, new_values, transform):
        self.scaler.partial_fit(new_values)
        self.array = np.concatenate([self.array[new_values.shape[1]:], new_values])
        self.values_scaler = self.scaler.transform(self.array)

