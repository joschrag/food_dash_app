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


# plus_btn_style = {
#     "color": "white",
#     "background-color": "#5fe515",
#     "font-size": "32pt",
#     "font-weight": "bold",
#     "border-radius": "0.5em",
#     "padding": "0.25em",
#     "width": "auto",
#     "aspect-ratio": "1 / 1",
#     "text-align": "center",
#     "vertical-align": "middle",
#     "border": "none",
# }

# plus_button = html.Button("+", id="plus_button_inv", style=plus_btn_style)
row_style = {"float": "left", "margin": "1em"}
inp_style = {**row_style, "max-width": "10em"}
btn_style = {
    **inp_style,
    "max-width": "10em",
    "background": "#5bc0de",
    "padding": "0.25em 0.5em",
    "color": "black",
    "border-radius": "0.5em",
    "border": "none",
}
dd_style = {**inp_style, "margin-right": "3em"}
name_txt = html.P("Item name:", style=row_style)
amount_txt = html.P("number of items:", style=row_style)
cat_dd = dcc.Dropdown(
    placeholder="Choose a category", searchable=True, style=dd_style
)
amount_inp = dcc.Input(id="inv_amount", type="number", step=1, style=inp_style)
name_inp = dcc.Input(id="inv_name", type="text", style=inp_style)
submit = dcc.ConfirmDialogProvider(
    children=html.Button("Submit", style=btn_style),
    id="inv_submit",
    message="Confirm your submission.",
)

add_item = html.Div(
    children=[name_txt, name_inp, cat_dd, amount_txt, amount_inp, submit],
    id="add_to_inventory",
    style={
        "min-witdh": "100px",
        "width": "80em",
        "min-height": "100px",
        "padding": "1em",
        "padding-left": "3em",
        "display": "inline-block",
    },
)

layout = dbc.Container([headline, add_item], fluid=True)
