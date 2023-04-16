"""
This module contains the layout for the navbar and the general app.

Author: Jonas Schrage
Date: 15.04.2023

"""
import dash
import dash_bootstrap_components as dbc
from dash import html

# Define the Dash app
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.SLATE, "assets/style.css"],
)
nav_link_style = {
    "margin": "1em 1em",
    "text-align": "center",
    "background": "#5bc0de",
    "padding": "0.5em 2em",
    "color": "black",
}

navbar = dbc.Navbar(
    [
        # Use row and col to control vertical alignment of logo / brand
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", style=nav_link_style),
                dbc.NavLink(
                    "Inventory", href="./inventory", style=nav_link_style
                ),
                dbc.NavLink("Meals", href="./meals", style=nav_link_style),
            ],
            vertical=False,
            pills=True,
        )
        # Another column, etc.
    ],
    color="dark",
    dark=True,
    sticky="top",
    style={
        "margin-left": "10em",
        "margin-bottom": "3em",
        "border": "none",
        "width": "auto",
    },
)

# Set the app layout
app.layout = dbc.Container(
    [
        navbar,
        dbc.Row(html.Div(dash.page_container)),
    ],
    className="dbc",
    fluid=True,
)
