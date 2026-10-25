-- SQLite Schema for Network Packet Routing Simulator

CREATE TABLE IF NOT EXISTS topologies (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    routers_json TEXT NOT NULL,
    links_json TEXT NOT NULL,
    is_default INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS packet_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    packet_id TEXT NOT NULL,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    algorithm TEXT NOT NULL,
    status TEXT NOT NULL,
    route_json TEXT,
    hops INTEGER DEFAULT 0,
    nodes_visited INTEGER DEFAULT 0,
    execution_time_ms REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
