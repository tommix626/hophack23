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
    radar_fig.update_layout(font=dict(
        size=27))
    radar_fig.update_layout(font_family="Impact",font_color="white")
    return radar_fig


def create_gauge_graph(data):
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=data,
        mode="gauge+number",  # "gauge+number+delta",
        title={'text': "Overall Score", 'font': {'size': 34}},
        # delta={'reference': last_score},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "#7f7f7f"},

               'steps': [
                   {'range': [0, 33], 'color': "#f5a4a4"},
                   {'range': [33, 66], 'color': "#f7f3cb"},
                   {'range': [66, 100], 'color': "#cef5d8"},
               ]}))
    fig.update_layout(font=dict(
        size=25))
    fig.update_layout(font_family="Impact",font_color="white")
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
], style={'background-image': 'url(data:image/jpeg;base64,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)',
          'background-size': '100%',
          'width': '100%',
          'height': '100%'
          })

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
    # Render the output.html template with the value of the txt variable
    return reader


def construct_data(reader):
    # print()
    # construct the ladar graph data
    df = pd.DataFrame(dict(
        r=[reader.accuracy_score, 10 - reader.aggressive_score, 10 - reader.satire_score, reader.credibility_score,
           reader.objective_score],
        theta=['Accuracy', 'Neutrality', 'Readability',
               'Credibility', 'Objectivity']))
    radar_fig = create_radar_graph(df)
    avg_score = ((reader.accuracy_score) + \
                 (10 - reader.aggressive_score) + \
                 (10 - reader.satire_score) + \
                 (reader.credibility_score) + \
                 (reader.objective_score)) * 2 + random.randint(
        -3, 3)

    tag_colors = ['#f5a4a4', '#f7f3cb', '#cef5d8', '#FF5722', '#673AB7', '#795548']
    genre_div = html.Div(className='article-box', children=[
        html.H3("Genre", style={'textAlign': 'center', 'font-family': 'Impact'}),
        html.Div(className='tag-container', style={'display': 'flex', 'flex-direction':'column', 'textAlign': 'center'}, children=[html.Div(className='tag', style={
            'border': '1px solid #ccc', 'padding': '5px 10px', 'margin': '5px','width': 'max-content',
            'background-color': tag_colors[i % len(tag_colors)], 'textAlign': 'center',
            'border-radius': '5px', 'color': '#333'}, children=e) for i, e in enumerate(reader.genre)]),
    ], style={'margin-left': '10px', 'margin-right': '10px', 'margin-bottom': '20px', 'margin-top': '10px',
              'width':'33%', 'background-color':'#333', 'border-radius':'20px'})

    context_div = html.Div(className='article-box', children=[
        html.H3("Context", style={'textAlign': 'center', 'font-family': 'Impact'}),
        html.Div(className='tag-container', style={'display': 'flex', 'flex-direction':'column', 'textAlign': 'center'}, children=[html.Div(className='tag', style={
            'border': '1px solid #ccc', 'padding': '5px 10px', 'margin': '5px', 'width': 'max-content',
            'background-color': tag_colors[i % len(tag_colors)], 'textAlign': 'center',
            'border-radius': '5px', 'color': '#333'}, children=e) for i, e in enumerate(reader.context)]),
    ], style={'margin-left': '10px', 'margin-right': '10px', 'margin-bottom': '20px', 'margin-top': '10px',
              'width':'33%', 'background-color':'#333', 'border-radius':'20px'})

    audience_div = html.Div([
        html.H3('Audience', style={'textAlign': 'center', 'font-family': 'Impact'}),
        html.Div(reader.audience, style={'font-weight': 'bold', 'font-size': '20px', 'textAlign': 'center'})
    ], style={'margin-left': '10px', 'margin-right': '10px', 'margin-bottom': '20px', 'margin-top': '10px',
              'width':'33%', 'background-color':'#333', 'border-radius':'20px'})

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
                html.H3(explanation, style={'font-size': '16px', 'color': 'darkblue','font-style':'italics'}),
            ], style={'background-color': '#aaa', 'border-radius': '10px', 'padding': '20px',
                      'margin-bottom': '20px',
                      'box-shadow': '0px 2px 6px rgba(0, 0, 0, 0.1)'})
        ], style={'margin-left': '50px', 'margin-right': '50px', 'margin-bottom': '20px', 'margin-top': '20px'}) for
        (text, explanation) in reader.aggressive_pair]

    similar_sources = reader.get_similar_sources()
    sim_source_div = [
        html.Div([
            html.Div([
                html.H5("..." + text + "...", style={'font-weight': 'bold', 'font-size': '20px', 'color': 'darkred'}),
                html.H3(explanation, style={'font-size': '16px', 'color': 'darkblue', 'font-style':'italics'}),
            ], style={'background-color': '#b1b5b2', 'border-radius': '10px', 'padding': '20px',
                      'margin-bottom': '20px',
                      'box-shadow': '0px 2px 6px rgba(0, 0, 0, 0.1)'})
        ], style={'margin-left': '50px', 'margin-right': '50px', 'margin-bottom': '20px', 'margin-top': '20px'}) for
        (text, explanation) in similar_sources]

    # construct final data
    l_data = [[
        html.H1(children='Analytic Report', style={'textAlign': 'center', 'font-family': 'Impact'}),
        html.Div([
            html.Br(),
            html.Div([dcc.Graph(figure=radar_fig, style={})], style={'padding': 10, 'flex': 1, 'border-radius': '20px'}),
            html.Div([dcc.Graph(figure=create_gauge_graph(data=avg_score))], style={'padding': 10, 'flex': 1, 'border-radius': '20px'})
        ], style={'display': 'flex', 'flex-direction': 'row', 'border-radius':'20px'}
        ),

        html.Div([genre_div,
                  audience_div,
                  context_div,
        ], style={'display': 'flex', 'flex-direction': 'row'}),

        html.Div([
        html.Div(
            [html.H1("Inaccuracy Alerts",
                style={'font-family': 'Impact'}),
            html.Div(acc_data_div)],style={'width':'50%','background-color':'#333','text-align': 'center', 'font-size': '32px', 'padding-top': '20px', 'padding-bottom': '20px',
                       'margin-left': '17px', 'margin-right': '8px','color': 'white', 'border-radius': '20px'}),

        html.Div(
            [html.H1("Exaggeration Alerts",
                style={'font-family': 'Impact'}),
            html.Div(agg_data_div)],style={'width':'50%','background-color':'#333','text-align': 'center', 'font-size': '32px', 'padding-top': '20px', 'padding-bottom': '20px',
                       'margin-left': '9px', 'margin-right': '17px','color': 'white', 'border-radius': '20px'})
            ], style={'display':'flex', 'flex-direction': 'row'}),

        html.H1("Similar Resources",
                style={'text-align': 'center', 'font-size': '32px', 'padding-top': '20px', 'padding-bottom': '20px',
                       'color': 'white', 'border-radius': '20px',
                       'font-family': 'Impact'}),
        html.Div(sim_source_div)
    ]]
    return l_data


if __name__ == '__main__':
    bashapp.run(debug=True)
