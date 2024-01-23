import plotly.express as px
import pandas as pd
# from dash import Dash, dcc, html

df = pd.DataFrame(dict(
    r=[1, 5, 2, 2, 3],
    theta=['processing cost','mechanical properties','chemical stability',
           'thermal stability', 'device integration']))
fig = px.line_polar(df, r='r', theta='theta', line_close=True)
fig.update_traces(fill='toself')
fig.show()

#
# app = Dash()
# app.layout = html.Div([
#     dcc.Graph(figure=fig)
# ])