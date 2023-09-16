from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
# from dash import Dash, dcc, html

def create_radar_graph(dataframe):
    radar_fig = px.line_polar(dataframe, r='r', theta='theta', line_close=True)
    return radar_fig

def create_gauge_graph(data):
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=450,
        mode="gauge+number+delta",
        title={'text': "Speed"},
        delta={'reference': 380},
        gauge={'axis': {'range': [None, 500]},
               'steps': [
                   {'range': [0, 250], 'color': "lightgray"},
                   {'range': [250, 400], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))
    return fig


df = pd.DataFrame(dict(
    r=[1, 5, 2, 2, 3],
    theta=['processing cost', 'mechanical properties', 'chemical stability',
           'thermal stability', 'device integration']))
radar_fig = create_radar_graph(df)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Analytic Report', style={'textAlign':'center'}),
    dcc.Graph(figure=radar_fig,style={}),
    dcc.Graph(figure=create_gauge_graph(data=None))
])


if __name__ == '__main__':
    app.run(debug=True)
