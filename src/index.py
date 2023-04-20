"""
This module contains the layout for the navbar and the general app.

Author: Jonas Schrage
Date: 15.04.2023

"""
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

import src.app_callbacks  # noqa # pylint: disable=unused-import

SECOND = 1000
MINUTE = 60 * SECOND
MINUTES10 = 10 * MINUTE
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
                dbc.NavLink(
                    "Home", href="/", active="exact", style=nav_link_style
                ),
                dbc.NavLink(
                    "Inventory",
                    href="/inventory",
                    active="exact",
                    style=nav_link_style,
                ),
                dbc.NavLink(
                    "Meals",
                    href="/meals",
                    active="exact",
                    style=nav_link_style,
                ),
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
        "padding-left": "10em",
        "padding-bottom": "3em",
        "border": "none",
        "width": "auto",
    },
)

# Set the app layout
app.layout = dbc.Container(
    children=[
        navbar,
        dbc.Row(html.Div(dash.page_container)),
        dcc.Store(id="meal_data", storage_type="session"),
        dcc.Store(id="ingredient_data", storage_type="session"),
        dcc.Store(id="tag_data", storage_type="session"),
        dcc.Store(id="tag_ingredient_data", storage_type="session"),
        dcc.Interval(id="10_min", interval=MINUTES10),
    ],
    className="dbc",
    fluid=True,
)
