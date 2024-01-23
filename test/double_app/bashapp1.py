import urllib

import pandas as pd
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash
# from dash import Dash, dcc, html
from dash_bootstrap_templates import load_figure_template
from flask import request
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


bashapp = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


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


bashapp.layout = html.Div(
    [dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout_data = [[
    html.H1(children='Analytic Report', style={'textAlign': 'center'}),
    html.Div([
        html.Br(),
        html.Div(children=[dcc.Graph(figure=radar_fig, style={})], style={'padding': 10, 'flex': 1}),
        html.Div(children=[dcc.Graph(figure=create_gauge_graph(data=None))], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flex-direction': 'row'}
    )
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
        query_parameters = urllib.parse.parse_qs(search.split("?")[-1])
        print(query_parameters)
        if "url" in query_parameters:
            print(F"query_parameters[url] = "+query_parameters["url"][0])
            if(is_valid_url(query_parameters["url"][0])):
                #process openai api and return layout for data.
                return layout_data
            else:
                return [[
                    html.H1('404 - Page not found'),
                    html.P('The page you are looking for does not exist.'),
                ]]
        else:
            return [[
                html.H1('404 - Page not found'),
                html.P('The page you are looking for does not exist.'),
            ]]
    else:
        return [[
            html.H1('404 - Page not found'),
            html.P('The page you are looking for does not exist.'),
        ]]

#
# @bashapp.server.route('/api/callback/')
# def callback():
#     code = request.args.get('code')
#     # Generate the content you want to display in the new window/tab
#     content = "<h1>Hello from Bash App! Your code is"+ code + "</h1>"
#
#     # You can also include JavaScript to manipulate the new window/tab if needed
#     script = f"<script>alert('Bash App content loaded, CODE={code}');</script>"
#
#     return f"{content}{script}"
# @bashapp.server.route('/display_in_new_window', methods=['GET','POST'])
# def display_in_new_window():
#     # Generate the content you want to display in the new window/tab
#     content = "<h1>Hello from Bash App!</h1>"
#
#     # You can also include JavaScript to manipulate the new window/tab if needed
#     script = "<script>alert('Bash App content loaded');</script>"
#
#     return f"{content}{script}"


if __name__ == '__main__':
    bashapp.run(debug=True)
