import dash
from dash import html
import dash_bootstrap_components as dbc

# Define the Dash app
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        "https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/slate/bootstrap.min.css"
    ],
)


navbar = dbc.Navbar(
    dbc.Container(
        [
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(dbc.NavItem(dbc.NavLink("Home", href="/"))),
                    dbc.Col(
                        dbc.NavItem(
                            dbc.NavLink("Inventory", href="./inventory")
                        )
                    ),
                    dbc.Col(dbc.NavItem(dbc.NavLink("Meals", href="./meals"))),
                ]
            )
            # Another column, etc.
        ],
        fluid=True,
    ),
    color="dark",
    dark=True,
    sticky="top",
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

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
