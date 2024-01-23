import urllib

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
    html.Div(id='page-content'),
    dcc.Input(id='query-input', type='text', placeholder='Enter query parameter'),
    html.Button('Submit', id='submit-button')
])


# Define callback functions to update the page content based on the URL and query parameter
@app.callback(
    [Output('page-content', 'children'),
     Output('query-input', 'value')],
    [Input('url', 'pathname'),
     Input('url', 'search'),
     Input('submit-button', 'n_clicks')],
)
def display_page(pathname, search, n_clicks):
    print(f"pathname={pathname}, search={search}")
    query_parameters = urllib.parse.parse_qs(search)
    print(query_parameters)
    if n_clicks:
        return f'Page: {pathname}, Query Parameter: {query_param}', query_param
    else:
        return f'Page: {pathname}', ''


# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
