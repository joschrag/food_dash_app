"""
This module contains the layout for the inventory page.

Author: Jonas Schrage
Date: 15.04.2023

"""
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html

dash.register_page(
    __name__,
    path="/inventory",
    name="Inventory",
    title="Inventory",
    description="Inventory page.",  # image="img_home.png"
)

headline = html.H1("Inventory")


name_txt = html.P("Item name:", className="row-item")
amount_txt = html.P("number of items:", className="row-item")
dd_txt = html.P("Select or add tag", className="row-item")
tag_txt = html.P("selected tags:", className="row-item")

amount_inp = dcc.Input(
    id="inv_amount",
    type="number",
    step=1,
    className="row-input",
    placeholder=0,
)
name_inp = dcc.Input(
    id="inv_name",
    type="text",
    className="row-input",
    placeholder="Enter a name",
    list="list_inv_name",
)
submit = html.Button(
    "Submit", className="row-item submit-btn", id="inv_submit_btn"
)


inv_tag_dd = dcc.Dropdown(
    id="multi-dropdown",
    multi=True,
    placeholder="Select a tag",
)

inv_tag_input = dcc.Input(
    id="custom-tag-input",
    placeholder="Enter a custom tag",
    className="row-item",
)

inv_tag_submit_btn = html.Button(
    "Add tag", id="add-tag-button", className="row-item submit-btn"
)

inv_input_form = dbc.Form(
    [
        html.Datalist(
            id="list_inv_name",
            children=[],
        ),
        dbc.Row(
            [
                dbc.Col(name_txt, width=2),
                dbc.Col(dd_txt, width={"size": 2, "offset": 1}),
                dbc.Col(
                    tag_txt,
                    width={"size": 2, "offset": 2},
                ),
                dbc.Col(
                    amount_txt,
                    width=2,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(name_inp, width=2),
                dbc.Col(inv_tag_dd, width=2),
                dbc.Col(inv_tag_input, width=2),
                dbc.Col(
                    inv_tag_submit_btn,
                    width=1,
                ),
                dbc.Col(html.Div(id="added-tags"), width=2),
                dbc.Col(amount_inp, width=2),
                dbc.Col(submit, width=1),
            ]
        ),
    ],
    className="inv-input",
)


data = pd.DataFrame(
    {
        "id": [0, 1, 2, 3, 4],
        "item_name": [
            "Käse",
            "Gurke",
            "Tortellini",
            "Brötchen",
            "Tomaten (passiert)",
        ],
        "category": ["Kühlschrank", "Gemüse", "Nudeln", "Frühstück", "Nudeln"],
        "amount": [2, 4, 0, 17, 33],
    }
)


item_overview = html.Div(
    children=[
        html.H4("Item Overview:"),
        dbc.Row(dbc.Col(id="inv_list")),
    ],
    id="inv_item_overview",
)

layout = dbc.Container([headline, inv_input_form, item_overview], fluid=True)
