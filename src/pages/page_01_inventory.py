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
cat_dd = dcc.Dropdown(
    placeholder="Choose a category",
    searchable=True,
    className="row-item inv-dd",
)
amount_inp = dcc.Input(
    id="inv_amount", type="number", step=1, className="row-input"
)
name_inp = dcc.Input(id="inv_name", type="text", className="row-input")
submit = dcc.ConfirmDialogProvider(
    children=html.Button("Submit", className="row-item submit-btn"),
    id="inv_submit",
    message="Confirm your submission.",
)

add_item = html.Div(
    children=[
        html.H4("Add an item:"),
        name_txt,
        name_inp,
        cat_dd,
        amount_txt,
        amount_inp,
        submit,
    ],
    id="add_to_inventory",
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


def display_items(input_df: pd.DataFrame) -> html.Table:
    """Create a html table to display the dataframe items.

    Args:
        input_df (pd.DataFrame): input data

    Returns:
        html.Table: data formatted into html table
    """
    row_div = []
    input_df = input_df.drop(columns=["id"])
    col_group = html.Colgroup([html.Col() for _ in input_df.columns])
    cols = ["Item", "Category", "Amount"]
    table_head = html.Thead(html.Tr([html.Th(c) for c in cols]))
    for _, content in input_df.iterrows():
        item_name, cat, amount = content
        item_txt = html.Td(item_name)
        item_cat = html.Td(cat)
        item_amount = html.Td(amount)
        row_div.append(
            html.Tr([item_txt, item_cat, item_amount], className="row-hover")
        )
    table_body = html.Tbody(row_div)
    return html.Table([col_group, table_head, table_body], id="inv_item_list")


item_overview = html.Div(
    children=[
        html.H4("Item Overview:"),
        display_items(data),
    ],
    id="inv_item_overview",
)

layout = dbc.Container([headline, add_item, item_overview], fluid=True)
