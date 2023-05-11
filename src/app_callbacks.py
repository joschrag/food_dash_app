"""
This module contains the logic for dash callback triggering.

Author: Jonas Schrage
Date: 16.04.2023

"""
from pathlib import Path
from typing import Tuple

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, ctx, html  # , dcc

from sql.sql_handler import SQLHandler

# from src.scripts.load_sample_data import load_data

db_path = Path.cwd() / "sql" / "example.db"


def read_data(table_name: str) -> list:
    """Load table data and return it in a json friendly format.

    Args:
        table_name (str): table name

    Returns:
        list: list of data from table
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
def load_tags(_: int, __: int) -> list:
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
def load_meals(_: int, __: int) -> list:
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
def load_ingredients(_: int, __: int) -> list:
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
def load_ingredient_tags(_: int, __: int) -> list:
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
def load_ingredient_meals(_: int, __: int) -> list:
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
    inputs={
        "n_clicks": Input("add-tag-button", "n_clicks"),
        "tag_data": Input("tag_data", "data"),
        "item_name": Input("inv_name", "value"),
    },
    state={
        "states": (
            State("multi-dropdown", "value"),
            State("multi-dropdown", "options"),
            State("custom-tag-input", "value"),
            State("ingredient_data", "data"),
            State("tag_ingredient_data", "data"),
        )
    },
)
def handle_dd_tags(
    n_clicks: int | None, tag_data: list, item_name: str, states: Tuple
) -> Tuple[list[str], list[dict[str, str]], str]:
    """Handle the selection of existing and addition of new tags.

    Args:
        n_clicks (int | None): number of button clicks
        tag_data (list): stored tag data
        item_name (str): name input value
        states (Tuple): multiple input states

    Returns:
        Tuple[list[str], list[dict[str, str]], str]: A tuple containing the
        updated value list, the updated options list and an the value of the new
        tag input field.
    """
    value: list
    options: list
    custom_tag: str
    item_data: list
    item_tag_data: list
    value, options, custom_tag, item_data, item_tag_data = states
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
    if ctx.triggered_id == "inv_name":
        if all([item_name, item_data, item_tag_data, tag_data]):
            item_df = pd.DataFrame(item_data)
            item_tag_df = pd.DataFrame(item_tag_data)
            tag_df = pd.DataFrame(tag_data)
            if item_name in item_df.ingredient_name.values:
                item_df = item_df.rename({"id": "ingredient_id"}, axis=1)
                tag_df = tag_df.rename({"id": "tag_id"}, axis=1)
                joint_df = item_df.merge(
                    item_tag_df, how="outer", on="ingredient_id"
                )
                joint_df = joint_df.merge(tag_df, how="outer", on="tag_id")
                value = joint_df.loc[
                    joint_df.ingredient_name == item_name, "tag_name"
                ].values.tolist()
            else:
                value = []

    options_list = pd.DataFrame(tag_data).tag_name.unique()
    options = [{"label": item, "value": item} for item in options_list]
    return value, options, custom_tag


@callback(
    Output("added-tags", "children"),
    Input("multi-dropdown", "value"),
)
def display_tags(selected_tags: list[str]) -> list[dbc.Badge] | None:
    """Display the selected tags as dbc Badges.

    Args:
        selected_tags (list[str]): The list of selected tags.

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
    ingredient_data: list, translate: list, tags: list
) -> list:
    """Display the ingredient inventory in a table.

    Args:
        ingredient_data (list): stored ingredient data
        translate (list): stored ingredient_id and tag_id data
        tags (list): stored tag data

    Returns:
        list: list containing the table to be shown
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
def update_ing_autocomplete(data: list) -> list:
    """Update the autocomlete suggestions.

    Args:
        data (list): data from store object

    Returns:
        list: list of html option tags
    """
    data_list = pd.DataFrame(data).ingredient_name.unique()
    return [html.Option(value=word) for word in data_list]


@callback(
    Output("reload_data_btn", "n_clicks"),
    inputs={
        "n_clicks": Input("inv_submit_btn", "n_clicks"),
        "name": State("inv_name", "value"),
        "amount": State("inv_amount", "value"),
        "tags": State("added-tags", "children"),
        "states": [
            State("tag_data", "data"),
            State("ingredient_data", "data"),
            State("tag_ingredient_data", "data"),
        ],
        "num_clicks": State("reload_data_btn", "n_clicks"),
    },
    prevent_initial_call=True,
)
def write_inventory_data(
    n_clicks: int,
    name: str,
    amount: float,
    tags: list,
    states: list,
    num_clicks: int,
) -> int:
    """Submit new inventory item to database and storage.

    Args:
        n_clicks (int): number of button clicks
        name (str): value of name input
        amount (float): value of amount input
        tags (list): selected tags

    Returns:
        Tuple[list, list, list]: Tuple of the updated store lists
    """
    num_clicks = num_clicks or 0
    amount = amount or 0
    if n_clicks and all(states):
        data: dict = {}
        tag_data, ingredient_data, tag_ingredient_data = states
        mem_tag_df = pd.DataFrame(tag_data)
        mem_ing_df = pd.DataFrame(ingredient_data)
        mem_tag_ing_df = pd.DataFrame(tag_ingredient_data)
        selected_tags = [tag.get("props").get("children") for tag in tags]
        new_tags = [
            tag
            for tag in selected_tags
            if tag not in mem_tag_df.tag_name.to_list()
        ]
        if new_tags:
            tags_df = pd.DataFrame({"tag_name": new_tags})
            data["tags"] = tags_df
        is_new_ingredient = name not in mem_ing_df.ingredient_name.to_list()
        if is_new_ingredient:
            ingredients_df = pd.DataFrame(
                {
                    "ingredient_name": [name],
                    "inventory_amount": [amount],
                }
            )
            data["ingredients"] = ingredients_df
            name_id = mem_ing_df.id.max() + 1
        else:
            name_id_arr = mem_ing_df.query("ingredient_name==@name").id.values
            assert len(name_id_arr) == 1
            name_id = name_id_arr[0]
            sql_handler = SQLHandler(db_path, "ingredients")
            assert sql_handler.sqltable is not None
            old_amount_arr = mem_ing_df.query(
                "id == @name_id"
            ).inventory_amount.values
            assert len(old_amount_arr) == 1
            old_amount = old_amount_arr[0]
            mem_ing_df.loc[mem_ing_df.id == name_id, "inventory_amount"] = (
                old_amount + amount
            )
            sql_handler.write_table(mem_ing_df, if_exists="replace")

        # filter old tags from the tag list
        old_tag_list = mem_tag_ing_df.query(
            "ingredient_id==@name_id"
        ).tag_id.values
        selected_tag_list = mem_tag_df.query(
            "tag_name in @selected_tags"
        ).id.values
        new_tags = [tag for tag in selected_tag_list if tag not in old_tag_list]
        ingredient_tag_df = pd.DataFrame(
            {
                "tag_id": new_tags,
                "ingredient_id": [name_id] * len(new_tags),
            }
        )

        data["ingredient_tags"] = ingredient_tag_df
        print(data)
        # if data:
        #    load_data(db_path, data)
    return num_clicks + 1
