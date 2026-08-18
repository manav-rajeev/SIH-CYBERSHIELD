"""Small SQLite layer that can be replaced by PostgreSQL later."""
import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("cybershield.db")


def get_connection(db_path: str | Path = DB_PATH):
    """Open a SQLite connection with row dictionaries enabled."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: str | Path = DB_PATH) -> None:
    """Create simple MVP tables for future persistence."""
    with get_connection(db_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS assets (
                asset_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id TEXT PRIMARY KEY,
                payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS security_events (
                event_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS incidents (
                incident_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS action_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id TEXT,
                payload TEXT NOT NULL
            );
            """
        )


def upsert_json_rows(table: str, key_field: str, rows: list[dict], db_path: str | Path = DB_PATH) -> None:
    """Persist dictionaries as JSON payloads while keeping schema beginner-friendly."""
    allowed_tables = {"assets", "vulnerabilities", "security_events", "incidents"}
    if table not in allowed_tables:
        raise ValueError(f"Unsupported table: {table}")
    with get_connection(db_path) as connection:
        for row in rows:
            connection.execute(
                f"INSERT OR REPLACE INTO {table} ({key_field}, payload) VALUES (?, ?)",
                (row[key_field], json.dumps(row)),
            )
