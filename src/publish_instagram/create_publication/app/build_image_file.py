from src.view.figures.time_series.candles import Candlestick
import plotly.graph_objects as go

class BuildImageFile:
    
    def __init__(self, infraestructure_data_connector):
        self._infraestructure_data_connector = infraestructure_data_connector
        
    
    def __call__(self, data: dict):
        icon = self._infraestructure_data_connector.get_icon(data['name'])
        color_candlestick = self._infraestructure_data_connector.get_color_candlestick(**data)
        cand = Candlestick.from_dataframe(data['dataframe'], **color_candlestick)
        layout = self._infraestructure_data_connector.get_layout(data['name'])
        fig = go.Figure([cand], layout=dict(margin=dict(l=10, r=10, t=5, b=5)))
        fig.add_layout_image(
            dict(
                source=icon,
                xref="paper", yref="paper",
                x=1, y=1.1,
                sizex=0.2, sizey=0.2,
                xanchor="right", yanchor="bottom"
            )
        )
        fig.update_layout(**layout)
        path_local_image = self._infraestructure_data_connector.save_local_image(fig, data)
        return path_local_image