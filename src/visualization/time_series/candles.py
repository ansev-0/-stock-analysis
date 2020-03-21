import plotly.graph_objects as go
import pandas as pd
import numpy as np

class Candlestick(go.Candlestick):
    @classmethod
    def from_dataframe(cls, dataframe, **kwargs):
        return cls(x=dataframe.index, **dict(dataframe.items()), **kwargs)


        
class FigureCandlestickManyDataFrame(go.Figure):
    
    def __init__(self, dict_dataframe, dict_colors=None, **kwargs):
        self.__dict_colors = dict_colors
        func_colors = self.__get_function_colors()
        data = [Candlestick.from_dataframe(dataframe=dataframe, name = company,
                                                 **func_colors(company))
                      for company, dataframe in dict_dataframe.items()]
        super().__init__(data=data, **kwargs)
        
    def _get_random_colors(self):
        return dict(zip(['increasing_line_color', 'decreasing_line_color'],
                        list(map(self._mapper_rgb_randomint,
                                 np.random.randint(low=0,
                                                   high=256,
                                                   size=(2,3))))))

    def __get_function_colors(self):
        if self.__dict_colors:
            return lambda company: self.dict_colors[company]
        return lambda *args : self._get_random_colors()
    
    
    @staticmethod
    def _mapper_rgb_randomint(x):
        rgb_code = ','.join(map(str, x))
        return f'rgb({rgb_code})'
    
