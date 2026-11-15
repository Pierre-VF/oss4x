"""
Module to manage a database input
"""

from datetime import datetime
from typing import Optional

import pandas as pd
from sqlmodel import Field, SQLModel

from oss4x.src.database import get_engine


# -------------------------------------------------------------------------------------
# Models
# -------------------------------------------------------------------------------------
def _primary_key():
    return Field(default=None, primary_key=True, nullable=False)


class RequestLog(SQLModel, table=True):
    id: int | None = _primary_key()
    referer: str | None
    timestamp: datetime
    channel: str | None


class SearchLog(SQLModel, table=True):
    id: int | None = _primary_key()
    search_term: str | None
    timestamp: datetime
    number_of_results: int
    view_offset: int | None


# A quick and dirty dumping of the database as JSON
def dump_database_request_log_as_csv() -> str:
    return pd.read_sql_table(RequestLog.__tablename__, get_engine()).to_csv(index=False)


def dump_database_search_log_as_csv() -> str:
    return pd.read_sql_table(SearchLog.__tablename__, get_engine()).to_csv(index=False)
