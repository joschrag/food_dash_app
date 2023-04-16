"""
This module contains the logic for dash callback triggering.

Author: Jonas Schrage
Date: 16.04.2023

"""
from typing import Dict, List, Tuple, Union

import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback


@callback(
    Output("multi-dropdown", "value"),
    Output("multi-dropdown", "options"),
    Output("custom-tag-input", "value"),
    Input("add-tag-button", "n_clicks"),
    State("multi-dropdown", "value"),
    State("multi-dropdown", "options"),
    State("custom-tag-input", "value"),
)
def add_new_tag(
    n_clicks: Union[int, None],
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
    value = value or []
    if n_clicks:
        added_tags = []
        if custom_tag:
            options.append({"label": custom_tag, "value": custom_tag})
            value.append(custom_tag)
            added_tags.append(custom_tag)
        return value, options, ""
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
    return None
