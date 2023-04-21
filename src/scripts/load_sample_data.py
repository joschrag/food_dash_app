"""
This script loads sample data to a local sqlite instance.

Author: Jonas Schrage
Date: 17.04.2023

"""
from pathlib import Path
from typing import Dict

import pandas as pd
import sqlalchemy as sa
from pandas.core.frame import DataFrame
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)

from sql.sql_handler import SQLHandler


def create_database(db_location: str | Path) -> None:
    """
    Create the SQLite database and define the tables.

    Args:
        db_location (str): The file location for the SQLite database.

    """
    # Define the SQLAlchemy engine

    sql_handler = SQLHandler(db_location)

    engine = sql_handler.engine

    # Define the tags table

    metadata = MetaData()

    _ = Table(
        "tags",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("tag_name", String),
    )

    # Define the meals table
    _ = Table(
        "meals",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String),
    )

    # Define the ingredients table
    _ = Table(
        "ingredients",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("ingredient_name", String),
        Column("inventory_amount", Float),
    )

    _ = Table(
        "ingredient_tags",
        metadata,
        Column(
            "ingredient_id",
            Integer,
            ForeignKey("ingredients.id"),
            primary_key=True,
        ),
        Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
    )

    _ = Table(
        "ingredient_meals",
        metadata,
        Column("meal_id", Integer, ForeignKey("meals.id"), primary_key=True),
        Column(
            "ingredient_id",
            Integer,
            ForeignKey("ingredients.id"),
            primary_key=True,
        ),
        Column("recipe_amount", Float),
    )

    # Create the database
    metadata.create_all(engine)


def load_data(db_location: str | Path, data: Dict[str, DataFrame]) -> None:
    """
    Load sample data into the SQLite database.

    Args:
        db_location (str): The file location for the SQLite database.
        data (dict): A dictionary containing DataFrames of sample data.
    """
    # Load the data into the database
    sql_handler = SQLHandler(db_location)

    engine = sql_handler.engine

    for table_name, iter_df in data.items():
        with engine.connect() as conn, conn.begin():
            print(table_name, iter_df, sep="\n")
            # iter_df.to_excel(f"{table_name}.xlsx")
            ingredients_table = None
            if table_name == "tags":
                iter_df.to_sql(
                    table_name, conn, if_exists="append", index=False
                )
            else:
                if table_name != "ingredients":
                    ingredients_table = sql_handler.get_table("ingredients")
                tag_table = sql_handler.get_table("tags")
                # print(iter_df)
                # Replace tag_name column with tag_id by querying the tags table
                if "tag_name" in iter_df.columns:
                    iter_df = tag_name_to_id(iter_df, tag_table, conn)
                print(iter_df)
                if (
                    "ingredient_name" in iter_df.columns
                    and table_name != "ingredients"
                ):
                    iter_df = ingredient_name_to_id(
                        iter_df, ingredients_table, conn
                    )
            iter_df.to_sql(table_name, conn, if_exists="append", index=False)


def ingredient_name_to_id(
    data: pd.DataFrame, table: sa.Table | None, conn: sa.Connection
) -> pd.DataFrame:
    """Replace the names given by ids present in the sql table.

    Args:
        data (pd.DataFrame): dataframe with item names
        table (sa.Table | None): table to get the ids from
        conn (sa.Connection): db connection

    Returns:
        pd.DataFrame: dataframe with item ids
    """
    ingredient_list = []
    assert table is not None
    for row in data.ingredient_name:
        stmt = sa.select(table.c.id).where(table.c.ingredient_name == row)
        ingredient_name_row = conn.execute(stmt).first()
        assert ingredient_name_row
        ingredient_name = ingredient_name_row[0]
        ingredient_list.append(ingredient_name)
    data["ingredient_id"] = pd.Series(ingredient_list)
    data = data.drop("ingredient_name", axis=1)
    return data


def tag_name_to_id(
    data: pd.DataFrame, table: sa.Table | None, conn: sa.Connection
) -> pd.DataFrame:
    """Replace the names given by ids present in the sql table.

    Args:
        data (pd.DataFrame): dataframe with item names
        table (sa.Table | None): table to get the ids from
        conn (sa.Connection): db connection

    Returns:
        pd.DataFrame: dataframe with item ids
    """
    print(conn, type(conn))
    tag_list = []
    assert table is not None
    for row in data.tag_name:
        stmt = sa.select(table.c.id).where(table.c.tag_name == row)
        tag_name_row = conn.execute(stmt).first()
        assert tag_name_row
        tag_name = tag_name_row[0]
        tag_list.append(tag_name)
    data["tag_id"] = pd.Series(tag_list)
    data = data.drop("tag_name", axis=1)
    return data


def main() -> None:
    """Initialize the database."""
    db_path = Path.cwd() / "sql" / "example.db"

    tags_df = pd.DataFrame(
        {"tag_name": ["Obst", "Gemüse", "Ersatzprodukt", "Kühlschrank"]}
    )

    meals_df = pd.DataFrame(
        {"name": ["Obstsalat", "Gemüsesuppe", "Bauerntopf"]}
    )

    ingredients_df = pd.DataFrame(
        {
            "ingredient_name": [
                "Apfel",
                "Banane",
                "Karotte",
                "Hackfleisch",
                "Paprika",
            ],
            "inventory_amount": [2, 1, 2, 1, 2],
        }
    )

    ingredient_tag_df = pd.DataFrame(
        {
            "tag_name": [
                "Obst",
                "Obst",
                "Gemüse",
                "Kühlschrank",
                "Ersatzprodukt",
                "Kühlschrank",
                "Gemüse",
                "Kühlschrank",
            ],
            "ingredient_name": [
                "Apfel",
                "Banane",
                "Karotte",
                "Karotte",
                "Hackfleisch",
                "Hackfleisch",
                "Paprika",
                "Paprika",
            ],
        }
    )

    meal_ingredient_df = pd.DataFrame(
        {
            "meal_id": [1, 1, 2, 3, 3, 3],
            "ingredient_id": [1, 2, 3, 3, 4, 5],
            "recipe_amount": [1.5, 2, 0.5, 1, 3.5, 2.5],
        }
    )

    all_data = {
        "tags": tags_df,
        "meals": meals_df,
        "ingredients": ingredients_df,
        "ingredient_tags": ingredient_tag_df,
        "ingredient_meals": meal_ingredient_df,
    }

    create_database(db_path)
    load_data(db_path, all_data)
