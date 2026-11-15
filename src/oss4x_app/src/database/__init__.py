"""
Module to manage a database input
"""

import os
from datetime import datetime
from typing import Optional

import pandas as pd
from oss4x.src.config import SETTINGS
from sqlmodel import Field, Session, SQLModel, create_engine


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


# -------------------------------------------------------------------------------------
# Engine and app database connection
# -------------------------------------------------------------------------------------


def _open_engine_and_create_database_if_missing():
    x = create_engine(
        SETTINGS.database_connection_string,
        echo=False,
    )
    # TODO : this currently also creates empty tables for the "oss4x" part of the code,
    #   this is likely avoidable and could be removed in a later version
    SQLModel.metadata.create_all(x)
    return x


_ENGINE = _open_engine_and_create_database_if_missing()


def open_database_session() -> Session:
    return Session(_ENGINE)


# A quick and dirty dumping of the database as JSON
def dump_database_request_log_as_csv() -> str:
    return pd.read_sql_table(RequestLog.__tablename__, _ENGINE).to_csv(index=False)


def dump_database_search_log_as_csv() -> str:
    return pd.read_sql_table(SearchLog.__tablename__, _ENGINE).to_csv(index=False)
