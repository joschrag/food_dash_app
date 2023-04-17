"""
This module contains the class for interacting with a local sqlite instance.

Author: Jonas Schrage
Date: 17.04.2023

"""
from pathlib import Path
from typing import Literal

import pandas as pd
import sqlalchemy as sa


class SQLHandler:
    """Connect and query databases."""

    def __init__(
        self,
        db_path: Path | str,
        table: str,
    ) -> None:
        """Initialize the class.

        Args:
            db_path (Path | str): path to db file
            table (str): name of table
        """
        self.db_path = Path(db_path)
        self.table = table
        self.establish_connection()

    def establish_connection(self) -> None:
        """Establish connection to a database."""
        self.meta = sa.MetaData()

        self.engine = sa.create_engine(f"sqlite:///{self.db_path}")
        self.meta.reflect(self.engine, views=True)
        self.sqltable = self.get_table()

    def get_table(self) -> sa.Table:
        """Get a table from the sqlite db.

        Raises:
            KeyError: Table doesnt exist.

        Returns:
            sa.Table: table from sqlite db
        """
        if f"{self.table}" in self.meta.tables:
            return self.meta.tables[f"{self.table}"]
        else:
            raise KeyError(f"Table {self.table} does not exist.")

    def read_table(self) -> pd.DataFrame:
        """Read table or view from SQL server."""
        stmt = sa.select(self.sqltable)
        return_df = pd.read_sql(stmt, self.engine)
        return return_df

    def write_table(
        self,
        upload_df: pd.DataFrame,
        if_exists: Literal["replace", "append", "fail"] = "fail",
    ) -> None:
        """Write a table to an SQL database.

        Args:
            upload_df (pd.DataFrame): Dataframe to write to SQL database.
            if_exists (Literal["replace","append","fail"], optional): Behaviour
            if table exists already. Defaults to "fail".
        """
        assert if_exists in ["replace", "append", "fail"]
        upload_df.reset_index(drop=True).to_sql(
            self.sqltable.name,
            self.engine,
            if_exists=if_exists,
            index=False,
        )
