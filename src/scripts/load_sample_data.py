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

from src.sql_handler import SQLHandler


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
        Column("id", Integer, primary_key=True),
        Column("tag_name", String),
    )

    # Define the items table
    _ = Table(
        "items",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
        Column("amount", Float),
        Column("tag_name", String, ForeignKey("tags.tag_name")),
    )

    # Define the meals table
    _ = Table(
        "meals",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
    )

    # Define the ingredients table
    _ = Table(
        "ingredients",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
        Column("quantity", Integer),
        Column("meal_id", Integer, ForeignKey("meals.id")),
        Column("tag_name", String, ForeignKey("tags.tag_name")),
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

    with engine.connect() as conn, conn.begin():
        for table_name, iter_df in data.items():
            if table_name == "tags":
                iter_df = data["tags"]
                if not "id" in iter_df.columns:
                    iter_df = iter_df.reset_index()
                    iter_df = iter_df.rename(columns={"index": "id"})
                iter_df.to_sql(
                    table_name, conn, if_exists="replace", index=False
                )
            else:
                tag_list = []
                tag_table = sql_handler.get_table("tags")
                # Replace tag_name column with tag_id by querying the tags table
                if "tag_name" in iter_df.columns:
                    for row in iter_df.tag_name:
                        stmt = sa.select(tag_table.c.id).where(
                            tag_table.c.tag_name == row
                        )
                        tag_name_row = conn.execute(stmt).first()
                        assert tag_name_row
                        tag_name = tag_name_row[0]
                        tag_list.append(tag_name)
                    iter_df["tag_id"] = pd.Series(tag_list)
                    iter_df.drop("tag_name", axis=1, inplace=True)
            if not "id" in iter_df.columns:
                iter_df = iter_df.reset_index()
                iter_df = iter_df.rename(columns={"index": "id"})
            iter_df.to_sql(table_name, conn, if_exists="replace", index=False)


if __name__ == "__main__":
    db_path = Path.cwd() / "sql" / "example.db"

    tags_df = pd.DataFrame({"tag_name": ["fruit", "vegetable", "meat"]})

    items_df = pd.DataFrame(
        {
            "name": ["apple", "banana", "carrot", "beef", "chicken"],
            "amount": [1.5, 2, 0.5, 3.5, 2.5],
            "tag_name": ["fruit", "fruit", "vegetable", "meat", "meat"],
        }
    )

    meals_df = pd.DataFrame(
        {"name": ["fruit salad", "vegetable soup", "beef stew"]}
    )

    ingredients_df = pd.DataFrame(
        {
            "name": ["apple", "banana", "carrot", "beef", "chicken"],
            "quantity": [2, 1, 2, 1, 2],
            "meal_id": [1, 2, 3, 3, 3],
            "tag_name": ["fruit", "fruit", "vegetable", "meat", "meat"],
        }
    )

    all_data = {
        "tags": tags_df,
        "items": items_df,
        "meals": meals_df,
        "ingredients": ingredients_df,
    }

    create_database(db_path)
    load_data(db_path, all_data)
