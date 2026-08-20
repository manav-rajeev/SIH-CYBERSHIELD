"""Persistence helpers for CyberShield browser detection history."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DB_PATH = (
    Path(__file__).resolve().parents[1]
    / "database"
    / "cybershield_history.db"
)


def _get_connection(
    db_path: str | Path = DB_PATH,
) -> sqlite3.Connection:
    """Create a SQLite connection for detection history."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_history_db(
    db_path: str | Path = DB_PATH,
) -> None:
    """Create the detection history table if it does not exist."""
    with _get_connection(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS detection_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                url TEXT NOT NULL,
                score INTEGER NOT NULL,
                classification TEXT NOT NULL,
                reasons TEXT NOT NULL,
                url_features TEXT NOT NULL,
                website_features TEXT NOT NULL
            )
            """
        )


def record_detection(
    result: dict[str, Any],
    db_path: str | Path = DB_PATH,
) -> dict[str, Any]:
    """Store one CyberShield detection result."""
    initialize_history_db(db_path)

    timestamp = datetime.now(timezone.utc).isoformat()

    with _get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO detection_history (
                timestamp,
                url,
                score,
                classification,
                reasons,
                url_features,
                website_features
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                str(result.get("url", "")),
                int(result.get("score", 0)),
                str(result.get("classification", "UNKNOWN")),
                json.dumps(result.get("reasons", [])),
                json.dumps(result.get("url_features", {})),
                json.dumps(result.get("website_features", {})),
            ),
        )

        detection_id = cursor.lastrowid

    return {
        "id": detection_id,
        "timestamp": timestamp,
        "url": result.get("url", ""),
        "score": result.get("score", 0),
        "classification": result.get(
            "classification",
            "UNKNOWN",
        ),
    }


def get_detection_history(
    limit: int = 50,
    db_path: str | Path = DB_PATH,
) -> list[dict[str, Any]]:
    """Return the most recent detection records."""
    if limit <= 0:
        return []

    initialize_history_db(db_path)

    with _get_connection(db_path) as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                timestamp,
                url,
                score,
                classification,
                reasons,
                url_features,
                website_features
            FROM detection_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    results = []

    for row in rows:
        results.append(
            {
                "id": row["id"],
                "timestamp": row["timestamp"],
                "url": row["url"],
                "score": row["score"],
                "classification": row["classification"],
                "reasons": json.loads(row["reasons"]),
                "url_features": json.loads(
                    row["url_features"]
                ),
                "website_features": json.loads(
                    row["website_features"]
                ),
            }
        )

    return results


def clear_detection_history(
    db_path: str | Path = DB_PATH,
) -> None:
    """Delete all stored browser detection records."""
    initialize_history_db(db_path)

    with _get_connection(db_path) as connection:
        connection.execute(
            "DELETE FROM detection_history"
        )