"""
This module contains the layout for the meals page.

Author: Jonas Schrage
Date: 15.04.2023

"""
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(
    __name__,
    path="/meals",
    name="Meals",
    title="Meals",
    description="Meals page.",  # image="img_home.png"
)

headline = html.H1("Meals")

meal_name_txt = html.P("meal name", className="grid grid-item")
comp_name_txt = html.P("ingridient name", className="grid grid-item")
amount_txt = html.P("ingridient amount", className="grid grid-item")
meal_name_inp = dcc.Input(
    type="text", placeholder="Enter a meal name...", className="grid grid-input"
)
comp_name_inp = dcc.Input(
    type="text",
    placeholder="Enter an ingridient name...",
    className="grid grid-input",
)
amount_inp = dcc.Input(
    type="number", placeholder=0, className="grid grid-input"
)

add_comp_btn = html.Button(
    "Add ingridients", className="grid grid-btn submit-btn"
)


add_meal_dbc = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(meal_name_txt, width=4),
                dbc.Col(comp_name_txt, width=4),
                dbc.Col(amount_txt, width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(meal_name_inp, width=4),
                dbc.Col(comp_name_inp, width=4),
                dbc.Col(amount_inp, width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(add_comp_btn, width={"size": 4, "offset": 8}),
            ]
        ),
    ],
    id="add_meal_div",
)
# TODO rewrite using forms
layout = dbc.Container([headline, add_meal_dbc], fluid=True)
