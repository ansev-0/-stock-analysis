from PIL import Image
from src.view.figures.time_series.candles import Candlestick
import plotly.graph_objects as go

def create_image(name, data, icon_path):
    img = Image.open(icon_path)
    cand = Candlestick.from_dataframe(data[['open', 'close', 'high', 'low']], 
                                      **{'increasing_line_color': 'rgb(255,0,0)',
                                         'decreasing_line_color': 'rgb(0,255,0)'})
    start = data.index[0]
    end = data.index[-1]
    fig = go.Figure([cand],    
                    **{'layout': go.Layout(margin=dict(l=10, r=10, t=5, b=5))})
    fig.update_layout(xaxis_rangeslider_visible=False, autosize=False, width=400, height=500)
    # Add icon
    fig.add_layout_image(
        dict(
            source=img,
            xref="paper", yref="paper",
            x=1, y=1.05,
            sizex=0.2, sizey=0.2,
            xanchor="right", yanchor="bottom"
        )
    )
    # update layout properties
    fig.update_layout(
        autosize=False,
        height=800,
        width=700,
        bargap=0.15,
        bargroupgap=0.1,
        barmode="stack",
        hovermode="x",
        margin=dict(r=20, l=2, b=75, t=150),

        title='<span style="font-size: 40px;font-weight: bold;">'\
            + f"{name} <br>"\
            + '<br>'\
            +  '<span style="font-size: 15px;font-weight: normal;">'\
            + f'From {start.date()} to {end.date()}</span>'

    )
    return fig
