import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

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
    className="row-item inv_dd",
)
amount_inp = dcc.Input(
    id="inv_amount", type="number", step=1, className="row-input"
)
name_inp = dcc.Input(id="inv_name", type="text", className="row-input")
submit = dcc.ConfirmDialogProvider(
    children=html.Button("Submit",className="row-item submit-btn"),
    id="inv_submit",
    message="Confirm your submission.",
)

add_item = html.Div(
    children=[name_txt, name_inp, cat_dd, amount_txt, amount_inp, submit],
    id="add_to_inventory",
)

layout = dbc.Container([headline, add_item], fluid=True)
