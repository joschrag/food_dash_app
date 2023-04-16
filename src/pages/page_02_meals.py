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

meal_name_txt = dbc.Label(
    html.P("meal name"), html_for="meal_inp", className="grid grid-item"
)
comp_name_txt = dbc.Label(
    html.P("ingredient name"), html_for="comp_inp", className="grid grid-item"
)
amount_txt = dbc.Label(
    html.P("ingredient amount"),
    html_for="amount_inp",
    className="grid grid-item",
)
meal_name_inp = dcc.Input(
    type="text",
    placeholder="Enter a meal name...",
    className="grid grid-input",
    id="meal_inp",
)
comp_name_inp = dcc.Input(
    type="text",
    placeholder="Enter an ingredient name...",
    className="grid grid-input",
    id="comp_inp",
)
amount_inp = dcc.Input(
    type="number", placeholder=0, className="grid grid-input", id="amount_inp"
)

add_comp_btn = html.Button(
    "Add ingredients", className="grid grid-btn submit-btn"
)

submit_meal_btn = html.Button(
    "Submit meal recipe", className="grid grid-btn submit-btn"
)


add_meal_dbc = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Col(meal_name_txt, width=4, class_name="grid"),
                dbc.Col(comp_name_txt, width=4, class_name="grid"),
                dbc.Col(amount_txt, width=4, class_name="grid"),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(meal_name_inp, width=4, class_name="grid"),
                dbc.Col(comp_name_inp, width=4, class_name="grid"),
                dbc.Col(amount_inp, width=4, class_name="grid"),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    add_comp_btn,
                    width={"size": 2, "offset": 8},
                    class_name="grid",
                ),
                dbc.Col(
                    submit_meal_btn,
                    width={"size": 2},
                    class_name="grid",
                ),
            ]
        ),
    ],
    id="add_meal_div",
)
layout = dbc.Container([headline, add_meal_dbc], fluid=True)
