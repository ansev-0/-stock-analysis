import numpy as np
import pandas as pd

class SplitStackedArray:
    
    def onebatch_list(self, array, index):
        return np.split(ary=array,
                        indices_or_sections=index,
                        axis=2)

    def onebatch_dict(self, array, index, labels):
        return dict(zip(labels, self.onebatch_list(list(array.values()), index)))

    def manybatch_dict(self, array, index, labels, batch_size):
        arrays_batches = self._split_in_batches(array, batch_size)
        return list(map(lambda array: dict(zip(labels, self.onebatch_list(array, index))),
                        arrays_batches))

    def manybatch_list(self, array, index , batch_size):
        arrays_batches = self._split_in_batches(array, batch_size)

        return list(map(lambda array: self.onebatch_list(array, index),
                        arrays_batches))

    def _split_in_batches(self, array, batch_size):
        return  np.split(ary=array, 
                         indices_or_sections=self._get_batch_index_split(array.shape[0], batch_size),
                         axis=0)

    @staticmethod
    def _get_batch_index_split(samples, batch_size):

        if samples % batch_size != 0:
            raise ValueError('all batches must be the same length')

        return (np.arange(samples // batch_size) * batch_size)[1:]




    