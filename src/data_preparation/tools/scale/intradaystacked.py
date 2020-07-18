from src.data_preparation.tools.expand.stacked_intraday_delay import StackAndMapIntradaySequences
from src.data_preparation.tools.expand.stacked_multifrecuency import MultiFrecuencyScaleAndStackSequences
from sklearn.preprocessing import StandardScaler
import pandas as pd


class ScalerStackedIntradaySequences(StackAndMapIntradaySequences):
    
    @StackAndMapIntradaySequences.stacked_sequences
    def standardscaler(self, array, with_std=False):
        scaler = StandardScaler(with_std=with_std)
        return scaler.fit_transform(array)



class MultiFrecuencyStandardScaleAndStackSequences(MultiFrecuencyScaleAndStackSequences):




    @MultiFrecuencyScaleAndStackSequences.wrap_array3d_from_dataframe(save_in='list')
    def arrays_scaled_from_dataframe(self, array, array_target=None, **kwargs):
        return self._scale_array_and_target(array, array_target)


    @MultiFrecuencyScaleAndStackSequences.wrap_array3d_from_dataframe(save_in='dict')
    def dict_arrays_scaled_from_dataframe(self, array, array_target=None, **kwargs):
        return self._scale_array_and_target(array, array_target)



    @MultiFrecuencyScaleAndStackSequences.wrap_from_serie(type_output='dataframe')
    def frames_scaled_from_serie(self, dataframe, dataframe_target=None, **kwargs):

        array_scaled, scaler = self._scale(dataframe)
        dataframe_scaled = pd.DataFrame(array_scaled, columns=dataframe.columns, index=dataframe.index)

        if dataframe_target is not None:
            return dataframe_scaled, pd.DataFrame(self._scale_target(dataframe_target, scaler),
                                                  columns=dataframe_target.columns,
                                                  index= dataframe_target.index), scaler

        return dataframe_scaled


    @MultiFrecuencyScaleAndStackSequences.wrap_from_serie(type_output='array')
    def arrays_scaled_from_serie(self, array, array_target=None, **kwargs):
        return self._scale_array_and_target(array, array_target)


    def _scale_array_and_target(self, array, array_target=None):
        array_scaled, scaler = self._scale(array)
        if array_target is not None:
            return array_scaled, self._scale_target(array_target, scaler), scaler
        return array_scaled


    def _scale(self, data):

        scaler=StandardScaler(with_std=False)
        data_scaled = scaler.fit_transform(data.T).T
        return data_scaled, scaler

    @staticmethod
    def _scale_target(target, scaler):
        return scaler.transform(target.T).T


