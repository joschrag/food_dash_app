"""
This module contains the logic for dash callback triggering.

Author: Jonas Schrage
Date: 16.04.2023

"""
from pathlib import Path
from typing import Dict, List, Tuple, Union

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, ctx, html  # , dcc

from sql.sql_handler import SQLHandler
from src.scripts.load_sample_data import load_data

db_path = Path.cwd() / "sql" / "example.db"


def read_data(table_name: str) -> List:
    """Load table data and return it in a json friendly format.

    Args:
        table_name (str): table name

    Returns:
        List: List of data from table
    """
    conn = SQLHandler(db_path, table_name)
    result = conn.read_table()
    assert result.size > 0
    return result.to_dict("records")


@callback(
    Output("tag_data", "data"),
    Input("10_min", "n_intervals"),
    Input("reload_data_btn", "n_clicks"),
)
def load_tags(_: int, __: int) -> List:
    """Load tags data from database and return as a list.

    Args:
        _ (int): Unused input, required for Dash callback.

    Returns:
        A list of tag data from the database.
    """
    return read_data("tags")


@callback(
    Output("meal_data", "data"),
    Input("10_min", "n_intervals"),
    Input("reload_data_btn", "n_clicks"),
)
def load_meals(_: int, __: int) -> List:
    """Load meals data from database and return as a list.

    Args:
        _ (int): Unused input, required for Dash callback.

    Returns:
        A list of meal data from the database.
    """
    return read_data("meals")


@callback(
    Output("ingredient_data", "data"),
    Input("10_min", "n_intervals"),
    Input("reload_data_btn", "n_clicks"),
)
def load_ingredients(_: int, __: int) -> List:
    """Load ingredients data from database and return as a list.

    Args:
        _ (int): Unused input, required for Dash callback.

    Returns:
        A list of ingredient data from the database.
    """
    return read_data("ingredients")


@callback(
    Output("tag_ingredient_data", "data"),
    Input("10_min", "n_intervals"),
    Input("reload_data_btn", "n_clicks"),
)
def load_ingredient_tags(_: int, __: int) -> List:
    """Load ingredients data from database and return as a list.

    Args:
        _ (int): Unused input, required for Dash callback.

    Returns:
        A list of ingredient data from the database.
    """
    return read_data("ingredient_tags")


@callback(
    Output("meal_ingredient_data", "data"),
    Input("10_min", "n_intervals"),
    Input("reload_data_btn", "n_clicks"),
)
def load_ingredient_meals(_: int, __: int) -> List:
    """Load ingredients data from database and return as a list.

    Args:
        _ (int): Unused input, required for Dash callback.

    Returns:
        A list of ingredient data from the database.
    """
    return read_data("ingredient_meals")


# @callback(
#     Output("reload_data_btn", "active"),
#     Input("meal_ingredient_data", "data"),
#     Input("ingredient_data", "data"),
#     Input("tag_ingredient_data", "data"),
#     Input("meal_data", "data"),
#     Input("tag_data", "data"),
# )
# def reset_button(*args):
#     _ = args
#     return False


@callback(
    Output("multi-dropdown", "value"),
    Output("multi-dropdown", "options"),
    Output("custom-tag-input", "value"),
    Input("add-tag-button", "n_clicks"),
    Input("tag_data", "data"),
    State("multi-dropdown", "value"),
    State("multi-dropdown", "options"),
    State("custom-tag-input", "value"),
)
def add_new_tag(
    n_clicks: Union[int, None],
    data: List,
    value: List[str],
    options: List[Dict[str, str]],
    custom_tag: str,
) -> Tuple[List[str], List[Dict[str, str]], str]:
    """Add new tag to the list of selected tags.

    Args:
        n_clicks (int or None): The number of times the 'add tag' button has
            been clicked.
        value (List[str]): The current list of selected tags.
        options (List[Dict[str, str]]): The current list of dropdown options.
        custom_tag (str): The custom tag entered by the user.

    Returns:
        A tuple containing the updated value list, the updated options list,
        and an empty string.
    """
    options = options or []
    value = value or []
    if ctx.triggered_id == "add-tag-button" and n_clicks:
        added_tags = []
        if custom_tag:
            conn = SQLHandler(db_path, "tags")
            options.append({"label": custom_tag, "value": custom_tag})
            value.append(custom_tag)
            added_tags.append(custom_tag)
            data_df = pd.DataFrame({"tag_name": [custom_tag]})
            conn.write_table(data_df, if_exists="append")
        return value, options, ""

    options_list = pd.DataFrame(data).tag_name.unique()
    options = [{"label": item, "value": item} for item in options_list]
    return value, options, ""


@callback(
    Output("added-tags", "children"),
    Input("multi-dropdown", "value"),
)
def display_tags(selected_tags: List[str]) -> List[dbc.Badge] | None:
    """Display the selected tags as dbc Badges.

    Args:
        selected_tags (List[str]): The list of selected tags.

    Returns:
        A list of dbc Badges, one for each selected tag.
    """
    if selected_tags:
        badges = [
            dbc.Badge(tag, className="tag-badge") for tag in selected_tags
        ]
        return badges
    return []


def display_items(input_df: pd.DataFrame) -> html.Table:
    """Create a html table to display the dataframe items.

    Args:
        input_df (pd.DataFrame): input data

    Returns:
        html.Table: data formatted into html table
    """
    row_div = []
    col_group = html.Colgroup([html.Col() for _ in input_df.columns])
    cols = ["Item", "Tags", "Amount"]
    table_head = html.Thead(html.Tr([html.Th(c) for c in cols]))
    iter_df = input_df.loc[
        :, ["id", "ingredient_name", "inventory_amount"]
    ].drop_duplicates()
    for _, content in iter_df.iterrows():
        uid, item_name, amount = content
        _ = uid
        tags = input_df.query("id == @uid").loc[:, "tag_name"]
        badges = html.Td(
            [dbc.Badge(tag, className="tag-badge") for tag in tags]
        )
        item_txt = html.Td(item_name)
        # item_cat = html.Td(cat)
        item_amount = html.Td(amount)
        row_div.append(
            html.Tr([item_txt, badges, item_amount], className="row-hover")
        )
    table_body = html.Tbody(row_div)
    return html.Table([col_group, table_head, table_body], id="inv_item_list")


@callback(
    Output("inv_list", "children"),
    Input("ingredient_data", "data"),
    Input("tag_ingredient_data", "data"),
    Input("tag_data", "data"),
)
def display_ingredient_inventory(
    ingredient_data: List, translate: List, tags: List
) -> List:
    """Display the ingredient inventory in a table.

    Args:
        ingredient_data (List): stored ingredient data
        translate (List): stored ingredient_id and tag_id data
        tags (List): stored tag data

    Returns:
        List: list containing the table to be shown
    """
    temp_df = pd.DataFrame(ingredient_data).loc[
        :, ["id", "ingredient_name", "inventory_amount"]
    ]
    translate_df = pd.DataFrame(translate)
    tags_df = pd.DataFrame(tags)
    temp_df = temp_df.merge(
        translate_df, left_on="id", right_on="ingredient_id"
    )
    temp_df = temp_df.merge(
        tags_df.rename(columns={"id": "tag_id"}), on="tag_id"
    )
    table = display_items(temp_df)
    return [table]


@callback(Output("list_inv_name", "children"), Input("ingredient_data", "data"))
def update_ing_autocomplete(data: List) -> List:
    """Update the autocomlete suggestions.

    Args:
        data (List): data from store object

    Returns:
        List: list of html option tags
    """
    data_list = pd.DataFrame(data).ingredient_name.unique()
    return [html.Option(value=word) for word in data_list]


@callback(
    Output("reload_data_btn", "n_clicks"),
    inputs=dict(
        n_clicks=Input("inv_submit_btn", "n_clicks"),
        name=State("inv_name", "value"),
        amount=State("inv_amount", "value"),
        tags=State("added-tags", "children"),
        states=[
            State("tag_data", "data"),
            State("ingredient_data", "data"),
            State("tag_ingredient_data", "data"),
        ],
        num_clicks=State("reload_data_btn", "n_clicks"),
    ),
    prevent_initial_call=True,
)
def write_inventory_data(
    n_clicks: int,
    name: str,
    amount: float,
    tags: List,
    states: List,
    num_clicks: int,
) -> int:
    """Submit new inventory item to database and storage.

    Args:
        n_clicks (int): number of button clicks
        name (str): value of name input
        amount (float): value of amount input
        tags (List): selected tags

    Returns:
        Tuple[List, List, List]: Tuple of the updated store lists
    """
    num_clicks = num_clicks or 0
    if n_clicks and all(states):
        data: dict = {}
        tag_data, ingredient_data, tag_ingredient_data = states
        stored_tag_df = pd.DataFrame(tag_data)
        stored_ingredient_df = pd.DataFrame(ingredient_data)
        stored_tag_ingredient_df = pd.DataFrame(tag_ingredient_data)
        selected_tags = [tag.get("props").get("children") for tag in tags]
        new_tags = [
            tag
            for tag in selected_tags
            if tag not in stored_tag_df.tag_name.to_list()
        ]
        if new_tags:
            tags_df = pd.DataFrame({"tag_name": new_tags})
            data["tags"] = tags_df
        pd.DataFrame(ingredient_data).info()
        pd.DataFrame(tag_ingredient_data).info()
        is_new_ingredient = (
            name not in stored_ingredient_df.ingredient_name.to_list()
        )
        if is_new_ingredient:
            ingredients_df = pd.DataFrame(
                {
                    "ingredient_name": [name],
                    "inventory_amount": [amount],
                }
            )
            data["ingredients"] = ingredients_df
            name_id = stored_ingredient_df.id.max() + 1
        else:
            name_id_arr = stored_ingredient_df.query(
                "ingredient_name==@name"
            ).id.values
            assert len(name_id_arr) == 1
            name_id = name_id_arr[0]
        # filter old tags from the tag list
        print(stored_ingredient_df)
        print(f"{name_id=}\n")
        old_tag_list = stored_tag_ingredient_df.query(
            "ingredient_id==@name_id"
        ).tag_id.values
        print(selected_tags)
        selected_tag_list = stored_tag_df.query(
            "tag_name in @selected_tags"
        ).id.values
        print(old_tag_list)
        print(selected_tag_list)
        print("*" * 20)
        print(stored_tag_ingredient_df)
        print(stored_tag_df)
        new_ingredient_tags = stored_tag_ingredient_df.ingredient_id.to_list()
        ingredient_tag_df = pd.DataFrame(
            {
                "tag_name": selected_tags,
                "ingredient_name": [name] * len(selected_tags),
            }
        )

        data["ingredient_tags"] = ingredient_tag_df
        # if data:
        #    load_data(db_path, data)
    return num_clicks + 1
