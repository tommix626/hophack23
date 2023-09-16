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


# code = request.args.get('code') #TODO
# loads the "darkly" template and sets it as the default
load_figure_template("cyborg")

# dash.register_page(
#     __name__,
#     path='/test',
#     title='Our Analytics Dashboard',
#     name='Our Analytics Dashboard'
# )

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

layout_data = html.Div([
    html.H1(children='Analytic Report', style={'textAlign': 'center'}),
    html.Div([
        html.Br(),
        html.Div(children=[dcc.Graph(figure=radar_fig, style={})], style={'padding': 10, 'flex': 1}),
        html.Div(children=[dcc.Graph(figure=create_gauge_graph(data=None))], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flex-direction': 'row'}
    )
])
@bashapp.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/data':
        return layout_data
    elif pathname == '/page2':
        return html.Div([
            html.H1('Page 2'),
            html.P('This is the content of Page 2.'),
        ])
    else:
        return html.Div([
            html.H1('404 - Page not found'),
            html.P('The page you are looking for does not exist.'),
        ])

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
