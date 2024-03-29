import pandas as pd
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
# from dash import Dash, dcc, html
from dash_bootstrap_templates import load_figure_template

# loads the "darkly" template and sets it as the default
load_figure_template("cyborg")

def create_radar_graph(dataframe):
    radar_fig = px.line_polar(dataframe, r='r', theta='theta', line_close=True)
    radar_fig.update_traces(fill='toself')
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

app=Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div([
    html.H1(children='Analytic Report', style={'textAlign':'center'}),
    dcc.Graph(figure=radar_fig,style={}),
    dcc.Graph(figure=create_gauge_graph(data=None))
])
app.layout = html.Div([
    html.H1(children='Analytic Report', style={'textAlign':'center'}),
    html.Div([
        html.Br(),
        html.Div(children=[dcc.Graph(figure=radar_fig,style={})], style={'padding': 10, 'flex': 1}),
        html.Div(children=[dcc.Graph(figure=create_gauge_graph(data=None))], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flex-direction': 'row'}
    )
])


if __name__ == '__main__':
    app.run(debug=True)
