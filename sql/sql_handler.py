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
        table: str | None = None,
    ) -> None:
        """Initialize the class.

        Args:
            db_path (Path | str): path to db file
            table (str): name of table, defaults to None
        """
        self.db_path = Path(db_path)
        self.table = table
        self.meta = sa.MetaData()

        self.engine = sa.create_engine(f"sqlite:///{self.db_path}")
        self.meta.reflect(self.engine, views=True)
        self.sqltable = None
        if self.table is not None:
            self.sqltable = self.get_table()

    def get_table(self, table_name: str | None = None) -> sa.Table:
        """Get a table from the sqlite db.

        Args:
            table_name (str | None): name of table, defaults to None.

        Raises:
            KeyError: Table doesnt exist.

        Returns:
            sa.Table: table from sqlite db
        """
        table = table_name or self.table
        if f"{table}" in self.meta.tables:
            return self.meta.tables[f"{table}"]
        raise KeyError(f"Table {table} does not exist.")

    def read_table(self, table_name: str | None = None) -> pd.DataFrame:
        """Read table or view from SQL server.

        Args:
            table_name (str | None, optional): table name. Defaults to None.

        Returns:
            pd.DataFrame: Dataframe with data from sql table
        """
        if self.sqltable is None:
            assert table_name
            self.sqltable = self.get_table(table_name)
        self.meta.reflect(self.engine, views=True)
        stmt = sa.select(self.sqltable)
        return_df = pd.read_sql(stmt, self.engine)
        return return_df

    def write_table(
        self,
        upload_df: pd.DataFrame,
        table_name: str | None = None,
        if_exists: Literal["replace", "append", "fail"] = "fail",
    ) -> None:
        """Write a table to an SQL database.

        Args:
            upload_df (pd.DataFrame): Dataframe to write to SQL database.
            table_name (str | None): table name, defaults to None.
            if_exists (Literal["replace","append","fail"], optional): Behaviour
            if table exists already. Defaults to "fail".
        """
        assert if_exists in ["replace", "append", "fail"]
        if self.sqltable is None:
            assert table_name
            self.sqltable = self.get_table(table_name)
        upload_df.reset_index(drop=True).to_sql(
            self.sqltable.name,
            self.engine,
            if_exists=if_exists,
            index=False,
        )
