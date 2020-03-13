import plotly.graph_objects as go
import pandas as pd

class Candlestick(go.Candlestick):
    @classmethod
    def from_dataframe(cls, dataframe, **kwards):
        return cls(x=dataframe.index, **dict(dataframe.items()), **kwards)


        