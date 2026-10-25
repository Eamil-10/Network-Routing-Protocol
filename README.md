# Network Packet Routing and Dynamic Path Management Using Data Structures and Graph Traversal Algorithms

**Short Name:** Network Routing Simulator  
**Academic Course:** Data Structures and Algorithms (DSA) Microproject  
**Academic Level:** Bachelor of Computer Science & Engineering (Semester 3)

---

## 1. Project Overview & Central Purpose

The **Network Routing Simulator** is an interactive, educational software application designed from the ground up to visually and tangibly demonstrate foundational **Data Structures and Algorithms (DSA)** concepts through computer network packet routing.

Unlike generic CRUD applications, this project is strictly an **educational algorithms laboratory**. Every major feature in the software has a direct, explicit DSA justification and implementation:

* **Graph Representation (CO5):** Adjacency List ($O(V + E)$ space) and Adjacency Matrix ($O(V^2)$ space).
* **Queue Data Structure (CO1):** Custom manual FIFO Queue (`enqueue`, `dequeue`, `peek`, `size`) driving both the router packet arrival buffer and the level-by-level frontier in Breadth-First Search (BFS).
* **Stack Data Structure (CO1):** Custom manual LIFO Stack (`push`, `pop`, `peek`, `size`) driving Depth-First Search (DFS) and displaying deterministic stack unwinding during backtracking.
* **Linked List Data Structure (CO2):** Custom Singly Linked List (`append`, `to_list`, `display`) chaining visited router nodes to maintain dynamic packet route history and transmission audits.
* **Graph Traversal Algorithms (CO5):** 
  * **BFS:** Explores level by level; guarantees the **minimum-hop route in an unweighted graph**.
  * **DFS:** Explores deeply along one branch; demonstrates recursion/stack mechanics and dead-end backtracking.
* **Search Algorithms (CO3):** Manual Linear Search ($O(n)$) vs Binary Search ($O(\log n)$) evaluated using exact comparison counts.
* **Dynamic Route Recalculation (CO5):** Simulates hardware router failures and severed links, automatically reconstructing alternative paths or signaling a graceful **NO ROUTE AVAILABLE** state.
* **Forwarding Table Simulation:** Compares dynamic graph traversal with traditional pre-computed table-based next-hop routing.


---

## 2. Strict Academic Integrity Standard

In compliance with academic evaluation and viva requirements:
* **NO external graph or shortest-path libraries** (e.g. NetworkX BFS/DFS, Dijkstra libraries, `scipy.sparse.csgraph`) are used for core traversal operations.
* All data structures (`CustomQueue`, `CustomStack`, `CustomLinkedList`, `NetworkGraph`) and traversal/search algorithms (`simulate_bfs`, `simulate_dfs`, `reconstruct_path`, `linear_search_routers`, `binary_search_routers`) are implemented **manually from first principles**.

Third-party libraries are limited strictly to UI visualization ([Cytoscape.js](https://cytoscape.org/), [Chart.js](https://www.chartjs.org/)), HTTP communication ([Flask](https://flask.palletsprojects.com/)), persistence ([SQLite](https://www.sqlite.org/)), and testing ([pytest](https://docs.pytest.org/)).

---

## 3. Technology Stack

* **Frontend:**
  * Semantic HTML5 & Vanilla CSS3 (clean, modern, educational light design system).
  * Vanilla JavaScript (ES6+ modular controllers, simulation playback engine, search visualizer).
  * [Cytoscape.js](https://js.cytoscape.org/) for interactive graph topology rendering, node dragging, and path highlighting.
  * [Chart.js](https://www.chartjs.org/) for traversal and search comparison charts.
* **Backend:**
  * Python 3.9+ with Flask RESTful API.
* **Database:**
  * SQLite 3 (`network_sim.db`) with schema for topology presets, packet transmission logs, and activity audit feeds.
* **Test Suite:**
  * `pytest` with 37 automated unit and integration tests covering all custom data structures and API routes.

---

## 4. Directory Structure

```text
Microproject-NRP/
├── app.py                     # Main Flask Application & REST API endpoints
├── pytest.ini                 # Pytest configuration with pythonpath
├── requirements.txt           # Python dependencies (Flask, pytest, pytest-cov)
├── network_sim.db             # SQLite local database
├── core_dsa/                  # MANUAL DATA STRUCTURES & ALGORITHMS (Viva Core)
│   ├── __init__.py            # Module exports
│   ├── queue.py               # Custom FIFO Queue (CO1)
│   ├── stack.py               # Custom LIFO Stack
│   ├── linked_list.py         # Custom Singly Linked List (CO2)
│   ├── graph.py               # Custom Graph, Adjacency List & Matrix
│   ├── traversal.py           # Manual BFS & DFS engines with step tracing
│   ├── search.py              # Manual Linear & Binary Search with comparison counters
│   ├── routing_table.py       # Forwarding table generator & next-hop simulator
│   └── packet.py              # Packet model & FIFO PacketQueueManager
├── database/                  # PERSISTENCE & PRESET SCENARIOS
│   ├── __init__.py
│   ├── db.py                  # SQLite database manager & log queries
│   ├── schema.sql             # SQL schema (topologies, packet_history, activity_logs)
│   └── seed_data.py           # Predefined test topologies (Mesh, Ring, Bridge, 15-Router)
├── static/                    # FRONTEND ASSETS
│   ├── css/
│   │   ├── style.css          # Curated educational light design system
│   │   └── animations.css     # Educational micro-animations (pop-in, slide, pulse)
│   ├── js/
│   │   ├── api.js             # REST API client
│   │   ├── cytoscape_view.js  # Cytoscape graph renderer & state highlighter
│   │   ├── simulation.js      # Interactive step-by-step playback engine (BFS & DFS)
│   │   ├── search_view.js     # Linear vs Binary search interactive runner
│   │   ├── performance_view.js# Traversal comparison charts & benchmarks
│   │   └── app.js             # Main orchestrator & UI tab coordinator
│   └── vendor/
│       ├── cytoscape.min.js   # Local offline copy of Cytoscape.js
│       └── chart.umd.min.js   # Local offline copy of Chart.js
├── templates/
│   └── index.html             # Single Page Application with 11 educational tabs
└── tests/                     # PYTEST UNIT & INTEGRATION TEST SUITE
    ├── test_queue.py          # FIFO queue operations
    ├── test_stack.py          # LIFO stack operations
    ├── test_linked_list.py    # Singly linked list operations
    ├── test_graph.py          # Graph representations & failure states
    ├── test_bfs.py            # Minimum-hop correctness & trace verification
    ├── test_dfs.py            # Deep exploration, stack tracking & backtracking
    ├── test_search.py         # Linear & Binary search comparison counts
    ├── test_dynamic_routing.py# Dynamic rerouting on router/link cuts & No-Route
    └── test_api.py            # Flask REST endpoints integration
```

---

## 5. Algorithmic Complexity Reference

| Data Structure / Algorithm | Time Complexity | Auxiliary Space | Educational Purpose & Context |
| :--- | :---: | :---: | :--- |
| **Breadth-First Search (BFS)** | $O(V + E)$ | $O(V)$ | Explores layer-by-layer using a FIFO queue. Guarantees the **minimum-hop route in an unweighted graph**. |
| **Depth-First Search (DFS)** | $O(V + E)$ | $O(V)$ | Explores deeply using a LIFO stack. Demonstrates backtracking and path divergence. |
| **Adjacency List** | Lookup: $O(\text{deg}(V))$ | $O(V + E)$ | Memory-efficient for sparse topologies; optimal for BFS/DFS neighbor iteration. |
| **Adjacency Matrix** | Query: $O(1)$ | $O(V^2)$ | 2D matrix of size $|V| \times |V|$; enables constant-time edge existence check. |
| **Linear Search** | $O(n)$ | $O(1)$ | Sequential scan of unsorted records; comparison count scales linearly with $n$. |
| **Binary Search** | $O(\log n)$ | $O(1)$ | Halves the search space per iteration; strictly requires sorted router keys. |
| **FIFO Queue** | $O(1)$ ops | $O(n)$ | Manages arriving packet buffers and BFS exploration frontier. |
| **LIFO Stack** | $O(1)$ ops | $O(n)$ | Explicitly maintains branch history and unwinds on dead ends during DFS. |
| **Singly Linked List** | Append: $O(1)$ | $O(n)$ | Dynamic node chaining for packet transmission audit history without reallocations. |

---

## 6. How to Run the Project Locally

### Prerequisites
* Python 3.9 or higher
* Modern web browser (Chrome, Edge, Safari, Firefox)

### Step 1: Set Up Virtual Environment & Dependencies
```bash
# Navigate to project directory
cd "/Users/eamil/Documents/Sem 3/DSA/Microproject-NRP"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Run Automated Tests
```bash
pytest
```
*Expected Output:* `37 passed in 0.09s`

### Step 3: Launch Web Application
```bash
python3 app.py
```
*Access the Simulator in your browser at:* **`http://127.0.0.1:5000`**

---

## 7. Interactive Features & Guide

1. **Dashboard:** Live stat cards, active topology preview, and real-time activity event logs.
2. **Topology Studio:** Interactive Cytoscape graph canvas. Drag routers to reposition, inspect Adjacency List ($O(V+E)$), and inspect Adjacency Matrix ($O(V^2)$).
3. **Packet Buffer (FIFO Queue):** Visual conveyor queue showing **FRONT** and **REAR** badges. Enqueue packets and watch them dequeue and route across the network.
4. **BFS Simulation:** Interactive step-by-step playback (`Start`, `Step`, `Pause`, `Resume`, `Reset`). Highlights current processing node (amber), queued nodes (sky blue), and visited nodes (teal). Displays the live `parent[child]` mapping and executes backward path reconstruction.
5. **DFS Simulation:** Interactive step-by-step playback with vertical LIFO stack. Displays warning alerts when dead ends are reached and stack backtracking occurs.
6. **BFS vs DFS Benchmark:** Side-by-side comparative table and Chart.js bar chart evaluating Hops, Nodes Visited, Steps, and Backtracking.
7. **Router Search:** Live comparison of Linear Search ($O(n)$) vs Binary Search ($O(\log n)$). Visualizes pointers (`low`, `mid`, `high`) and calculates the exact number of comparisons.
8. **Routing Table:** Generates traditional next-hop forwarding tables for any selected router and simulates hop-by-hop forwarding.
9. **Failure & Dynamic Rerouting:** Click any link or select any router to toggle failure state. Recalculate routes to observe dynamic path adaptation or the graceful **NO ROUTE AVAILABLE** alert.
10. **Packet History (Linked List):** Click "View Linked List" on any processed packet to inspect its node chain (`Hop 1: R1 → Hop 2: R2 → Hop 3: R4 → Hop 4: R6`).
11. **Viva Guide & DSA Concepts:** Quick-reference complexity tables and high-yield interview questions and answers.

---

## 8. High-Yield Viva Voce Questions & Answers

### Q1: Why does BFS guarantee a minimum-hop route, while DFS does not?
> **Answer:** BFS explores vertices layer by layer (distance 1, distance 2, etc.) using a FIFO queue. Because all communication links in an unweighted graph have equal cost, the first time BFS discovers the target destination router, it is impossible for a path with fewer edges to exist. In contrast, DFS explores deeply down a single branch before backtracking. Depending on neighbor exploration order, DFS may discover a circuitous 5-hop path even if an alternate 2-hop path exists.

### Q2: Why is "Number of Comparisons" used instead of milliseconds to compare search algorithms?
> **Answer:** For small datasets (e.g. 6 to 15 routers), CPU execution time is on the order of microseconds. Operating system task scheduling, background interrupts, and clock precision introduce non-deterministic timing noise. The number of key comparisons is an exact, reproducible mathematical metric that reflects $O(n)$ vs $O(\log n)$ computational complexity without hardware bias.

### Q3: How does path reconstruction work using the parent map?
> **Answer:** During graph traversal, whenever an unvisited router $v$ is discovered from router $u$, we store `parent[v] = u`. Once the destination is reached, we trace backwards:  
> `destination → parent[destination] → parent[parent[destination]] → ... → source`.  
> Reversing this backward sequence yields the exact forward route.

### Q4: How does dynamic rerouting handle network link or router failure?
> **Answer:** When a router or link fails, its operational status is set to `is_active = False`. The `get_neighbors(router_id, active_only=True)` method filters out inactive components. Traversal re-executes on the modified graph topology. If the graph is disconnected (e.g. severed bridge link), the queue exhausts without reaching the destination, and the simulator displays a graceful **NO ROUTE AVAILABLE** condition without crashing.
