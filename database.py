import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).resolve().parent / "airfare.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_fare_records():
    conn = get_connection()

    query = """
        SELECT *
        FROM fare_records
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


def load_index_values():
    conn = get_connection()

    query = """
        SELECT *
        FROM index_values
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


def get_tables():
    conn = get_connection()

    query = """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """

    tables = pd.read_sql_query(query, conn)
    conn.close()

    return tables["name"].tolist()