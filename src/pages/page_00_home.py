"""
This module contains the layout for the home page.

Author: Jonas Schrage
Date: 15.04.2023

"""
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


layout = dbc.Container([html.H1("Home")], fluid=True)
