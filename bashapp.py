import math
import random

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash_bootstrap_templates import load_figure_template
from gpt_api import GPTReader
import urllib
from dash import dcc, html
from dash.dependencies import Input, Output

# loads the "darkly" template and sets it as the default
load_figure_template("cyborg")

bashapp = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


def create_radar_graph(dataframe):
    radar_fig = px.line_polar(dataframe, r='r', theta='theta', line_close=True)
    radar_fig.update_traces(fill='toself')
    return radar_fig


def create_gauge_graph(data):
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=data,
        mode="gauge+number",  # "gauge+number+delta",
        title={'text': "Overall Score"},
        # delta={'reference': last_score},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "#353835"},

               'steps': [
                   {'range': [0, 33], 'color': "#f5a4a4"},
                   {'range': [33, 66], 'color': "#f7f3cb"},
                   {'range': [66, 100], 'color': "#cef5d8"},
               ]}))
    return fig


bashapp.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Loading(
        id="loading",
        type="circle",
        fullscreen=True,
        style={
            'background-color': '#333',  # Dark background color
            'color': '#fff',  # Text color
            'font-size': '24px',  # Text size
            'padding': '20px',
            'border-radius': '10px',
            'box-shadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
            'text-align': 'center',
            'z-index': '1000',  # Ensure it's on top of other elements
        },
        children=[html.Div(id='page-content')]
    )
])

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
def display_page(pathname, search):
    if pathname == '/data':
        print(f"pathname={pathname}, search={search}")
        query_parameters = urllib.parse.parse_qs(search.split("?")[1])
        print(query_parameters)
        if "url" in query_parameters:
            print(F"query_parameters[url] = " + query_parameters["url"][0])
            if (is_valid_url(query_parameters["url"][0])):
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
    # print()
    # construct the ladar graph data
    df = pd.DataFrame(dict(
        r=[reader.accuracy_score, 10 - reader.aggressive_score, 10 - reader.satire_score, reader.credibility_score,
           reader.objective_score],
        theta=['accuracy', 'neutrality', 'readability',
               'credibility', 'objectivity']))
    radar_fig = create_radar_graph(df)
    avg_score = ((reader.accuracy_score) + \
                 (10 - reader.aggressive_score) + \
                 (10 - reader.satire_score) + \
                 (reader.credibility_score) + \
                 (reader.objective_score)) * 2 + random.randint(
        -3, 3)

    tag_colors = ['#f5a4a4', '#f7f3cb', '#cef5d8', '#FF5722', '#673AB7', '#795548']
    genre_div = html.Div(className='article-box', children=[
        html.H3("Genre"),
        html.Div(className='tag-container', style={'display': 'flex'}, children=[html.Div(className='tag', style={
            'border': '1px solid #ccc', 'padding': '5px 10px', 'margin': '5px',
            'background-color': tag_colors[i % len(tag_colors)],
            'border-radius': '5px', 'color': '#333'}, children=e) for i, e in enumerate(reader.genre)]),
    ], style={'margin-left': '50px', 'margin-right': '50px', 'margin-bottom': '20px', 'margin-top': '20px'})

    context_div = html.Div(className='article-box', children=[
        html.H3("Context"),
        html.Div(className='tag-container', style={'display': 'flex'}, children=[html.Div(className='tag', style={
            'border': '1px solid #ccc', 'padding': '5px 10px', 'margin': '5px',
            'background-color': tag_colors[i % len(tag_colors)],
            'border-radius': '5px', 'color': '#333'}, children=e) for i, e in enumerate(reader.context)]),
    ], style={'margin-left': '50px', 'margin-right': '50px', 'margin-bottom': '20px', 'margin-top': '20px'})

    audience_div = html.Div([
        html.H3('Audience'),
        html.Div(reader.audience, style={'font-weight': 'bold', 'font-size': '20px'})
    ], style={'margin-left': '50px', 'margin-right': '50px', 'margin-bottom': '20px', 'margin-top': '20px'})

    # quotes on accuracy_pair
    acc_data_div = [
        html.Div([
            html.Div([
                html.H5("..." + text + "...", style={'font-weight': 'bold', 'font-size': '20px', 'color': 'darkred'}),
                html.H3(explanation, style={'font-size': '16px', 'color': 'darkblue'}),
            ], style={'background-color': '#b1b5b2', 'border-radius': '10px', 'padding': '20px',
                      'margin-bottom': '20px',
                      'box-shadow': '0px 2px 6px rgba(0, 0, 0, 0.1)'})
        ], style={'margin-left': '50px', 'margin-right': '50px', 'margin-bottom': '20px', 'margin-top': '20px'}) for
        (text, explanation) in reader.accuracy_pair
    ]
    # quotes on accuracy_pair
    agg_data_div = [
        html.Div([
            html.Div([
                html.H5("..." + text + "...", style={'font-weight': 'bold', 'font-size': '20px', 'color': 'darkred'}),
                html.H3(explanation, style={'font-size': '16px', 'color': 'darkblue'}),
            ], style={'background-color': '#b1b5b2', 'border-radius': '10px', 'padding': '20px',
                      'margin-bottom': '20px',
                      'box-shadow': '0px 2px 6px rgba(0, 0, 0, 0.1)'})
        ], style={'margin-left': '50px', 'margin-right': '50px', 'margin-bottom': '20px', 'margin-top': '20px'}) for
        (text, explanation) in reader.aggressive_pair]

    # construct final data
    l_data = [[
        html.H1(children='Analytic Report', style={'textAlign': 'center'}),
        html.Div([
            html.Br(),
            html.Div(children=[dcc.Graph(figure=radar_fig, style={})], style={'padding': 10, 'flex': 1}),
            html.Div(children=[dcc.Graph(figure=create_gauge_graph(data=avg_score))], style={'padding': 10, 'flex': 1})
        ], style={'display': 'flex', 'flex-direction': 'row'}
        ),

        html.Div(audience_div),

        html.Div(genre_div),

        html.Div(context_div),

        html.H1("Inaccuracy Alerts",
                style={'text-align': 'center', 'font-size': '32px', 'padding-top': '20px', 'padding-bottom': '20px',
                       'background-color': 'darkred', 'color': 'white', 'border-radius': '10px',
                       'font-family': 'Courier New'}),
        html.Div(acc_data_div),

        html.H1("Exaggeration Alerts",
                style={'text-align': 'center', 'font-size': '32px', 'padding-top': '20px', 'padding-bottom': '20px',
                       'background-color': 'darkred', 'color': 'white', 'border-radius': '10px',
                       'font-family': 'Courier New'}),
        html.Div(agg_data_div)
    ]]
    return l_data


if __name__ == '__main__':
    bashapp.run(debug=True)
