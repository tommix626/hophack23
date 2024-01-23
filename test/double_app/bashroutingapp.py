import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Create a Dash application instance
app = dash.Dash(__name__)

# Define the layout of the application
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Nav([
        dcc.Link('Page 1', href='/page1'),
        dcc.Link('Page 2', href='/page2'),
    ]),
    html.Div(id='page-content')
])

# Define callback functions to update the page content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/page1':
        return html.Div([
            html.H1('Page 1'),
            html.P('This is the content of Page 1.'),
        ])
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

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
