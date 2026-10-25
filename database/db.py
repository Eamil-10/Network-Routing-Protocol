"""
Database Manager for Network Packet Routing Simulator
======================================================
Academic Context:
SQLite provides lightweight, zero-configuration local persistence for:
1. Topology definitions and presets.
2. Packet transmission logs and audit history.
3. Recent activity feed for the Dashboard overview.
"""

import sqlite3
import json
import os
from typing import Dict, List, Any, Optional
from database.seed_data import PRESET_SCENARIOS

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "network_sim.db")
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_db_connection() -> sqlite3.Connection:
    """Create a database connection with dictionary-like row access."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize SQLite database tables and seed preset scenarios if empty."""
    with open(SCHEMA_FILE, "r") as f:
        schema_sql = f.read()

    with get_db_connection() as conn:
        conn.executescript(schema_sql)

        # Check if topologies table is seeded
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) AS cnt FROM topologies")
        row = cur.fetchone()
        if row and row["cnt"] == 0:
            for scenario_id, data in PRESET_SCENARIOS.items():
                cur.execute(
                    """
                    INSERT INTO topologies (id, name, description, routers_json, links_json, is_default)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        data["id"],
                        data["name"],
                        data["description"],
                        json.dumps(data["routers"]),
                        json.dumps(data["links"]),
                        data.get("is_default", 0)
                    )
                )
            # Add initial activity log
            cur.execute(
                "INSERT INTO activity_logs (event_type, message) VALUES (?, ?)",
                ("SYSTEM_INIT", "Database initialized with preset educational topologies.")
            )
            conn.commit()


def get_all_scenarios() -> List[Dict[str, Any]]:
    """Retrieve list of all stored scenarios."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, description, is_default, created_at FROM topologies ORDER BY is_default DESC, name ASC")
        rows = cur.fetchall()
        return [dict(r) for r in rows]


def get_scenario_by_id(scenario_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve topology definition by ID."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM topologies WHERE id = ?", (scenario_id,))
        row = cur.fetchone()
        if not row:
            return None
        data = dict(row)
        data["routers"] = json.loads(data["routers_json"])
        data["links"] = json.loads(data["links_json"])
        return data


def log_packet_transmission(packet_dict: Dict[str, Any]) -> None:
    """Record packet delivery or failure to the persistent history table."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO packet_history
            (packet_id, source, destination, algorithm, status, route_json, hops, nodes_visited, execution_time_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                packet_dict["packet_id"],
                packet_dict["source"],
                packet_dict["destination"],
                packet_dict["algorithm"],
                packet_dict["status"],
                json.dumps(packet_dict.get("route", [])),
                packet_dict.get("hops", 0),
                packet_dict.get("nodes_visited", 0),
                packet_dict.get("execution_time_ms", 0.0)
            )
        )
        conn.commit()


def log_activity(event_type: str, message: str) -> None:
    """Log an activity event for the dashboard feed."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO activity_logs (event_type, message) VALUES (?, ?)",
            (event_type, message)
        )
        conn.commit()


def get_recent_activities(limit: int = 12) -> List[Dict[str, Any]]:
    """Retrieve the latest activity events for the dashboard."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, event_type, message, timestamp FROM activity_logs ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cur.fetchall()
        return [dict(r) for r in rows]


def get_packet_history_from_db(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve recent packet history from database."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM packet_history ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            item = dict(r)
            item["route"] = json.loads(item["route_json"]) if item["route_json"] else []
            result.append(item)
        return result
