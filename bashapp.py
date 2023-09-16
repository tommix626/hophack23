import pandas as pd
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
# from dash import Dash, dcc, html
from dash_bootstrap_templates import load_figure_template
from gpt_api import GPTReader
import urllib
from dash import dcc, html
from dash.dependencies import Input, Output

# loads the "darkly" template and sets it as the default
load_figure_template("cyborg")

bashapp=Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

def create_radar_graph(dataframe):
    radar_fig = px.line_polar(dataframe, r='r', theta='theta', line_close=True)
    radar_fig.update_traces(fill='toself')
    return radar_fig

def create_gauge_graph(data):
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=56,
        mode= "gauge+number", #"gauge+number+delta",
        title={'text': "Overall Score"},
        delta={'reference': 56},
        gauge={'axis': {'range': [None, 100]},
               'steps': [
                   {'range': [0, 33], 'color': "lightgray"},
                   {'range': [33, 66], 'color': "gray"}],
               'threshold': {'line': {'color': "blue", 'width': 4}, 'thickness': 0.75, 'value': 60}}))
    return fig




bashapp.layout = html.Div(
    [dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# layout_data = [[
#     html.H1(children='Analytic Report', style={'textAlign': 'center'}),
#     html.Div([
#         html.Br(),
#         html.Div(children=[dcc.Graph(figure=radar_fig, style={})], style={'padding': 10, 'flex': 1}),
#         html.Div(children=[dcc.Graph(figure=create_gauge_graph(data=None))], style={'padding': 10, 'flex': 1})
#     ], style={'display': 'flex', 'flex-direction': 'row'}
#     )
# ]]
layout_404 = [[
                    html.H1('404 - Page not found'),
                    html.P('The page you are looking for does not exist.'),
                ]]

def is_valid_url(url):
    try:
        # Attempt to parse the URL
        result = urllib.parse.urlparse(url)

        # Check if the scheme (e.g., http, https) and the network location (e.g., example.com) are present
        if all([result.scheme, result.netloc]):
            return True
        else:
            return False
    except ValueError:
        return False





@bashapp.callback(
    [Output('page-content', 'children')],
    [Input('url', 'pathname'),
     Input('url', 'search')]
)
def display_page(pathname,search):
    if pathname == '/data':
        print(f"pathname={pathname}, search={search}")
        query_parameters = urllib.parse.parse_qs(search.split("?")[1])
        print(query_parameters)
        if "url" in query_parameters:
            print(F"query_parameters[url] = "+query_parameters["url"][0])
            if(is_valid_url(query_parameters["url"][0])):
                #TODO:process openai api and return layout for data.
                GPTreader = get_reader(query_parameters["url"][0])
                layout_data = construct_data(GPTreader)
                return layout_data

    return layout_404

def get_reader(user_input_link):
    # use the openai api
    reader = GPTReader()
    reader.run(user_input_link)
    print(reader.get_similar_sources())
    # Render the output.html template with the value of the txt variable
    return reader

def construct_data(reader):
    print()
    #construct the ladar graph data
    df = pd.DataFrame(dict(
        r=[reader.accuracy_score, reader.aggressive_score,reader.satire_score,reader.credibility_score,reader.objective_score],
        theta=['accuracy', 'aggressive_score', 'satire_score',
               'credibility_score', 'objective_score']))
    radar_fig = create_radar_graph(df)
    l_data = [[
    html.H1(children='Analytic Report', style={'textAlign': 'center'}),
    html.Div([
        html.Br(),
        html.Div(children=[dcc.Graph(figure=radar_fig, style={})], style={'padding': 10, 'flex': 1}),
        html.Div(children=[dcc.Graph(figure=create_gauge_graph(data=None))], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flex-direction': 'row'}
    )
]]
    return l_data


if __name__ == '__main__':
    bashapp.run(debug=True)
