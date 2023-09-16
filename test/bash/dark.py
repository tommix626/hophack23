from dash import Dash, dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# loads the "darkly" template and sets it as the default
load_figure_template("darkly")

df = px.data.tips()

fig = px.scatter(df, x="total_bill", y="tip", color="size")

app=Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.layout = dbc.Container([
    html.H1("Dash App in Dark Mode", className="text-center"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)