"""
This module contains the layout for the meals page.

Author: Jonas Schrage
Date: 15.04.2023

"""
import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(
    __name__,
    path="/meals",
    name="Meals",
    title="Meals",
    description="Meals page.",  # image="img_home.png"
)

layout = html.Div([dbc.Container([html.H1("Meals")], fluid=True)])
