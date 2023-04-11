import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(
    __name__,
    path="/",
    name="Home",
    title="Home",
    description="Landing page.",  # image="img_home.png"
)


layout = dbc.Container(
    [html.H1("Home")],
)
