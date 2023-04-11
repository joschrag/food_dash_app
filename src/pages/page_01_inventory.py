import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(
    __name__,
    path="/inventory",
    name="Inventory",
    title="Inventory",
    description="Inventory page.",  # image="img_home.png"
)

layout = html.Div([dbc.Container([html.H1("Inventory")], fluid=True)])
