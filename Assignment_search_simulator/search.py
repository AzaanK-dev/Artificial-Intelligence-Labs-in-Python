"""
Search Algorithm Simulator (terminal-based, no external libraries)
Algorithms: Random Search, BFS, DFS, IDS, UCS
"""

import random
from collections import deque

# ----------------------------------------------------------------------
# DEMO GRAPH (undirected, weighted). Format: (node1, node2, cost)
#
#   Fewest edges  S -> B -> G            = 2 edges, cost 15  (BFS/IDS find this)
#   Cheapest path S -> A -> C -> D -> G  = 4 edges, cost 8   (UCS finds this)
#   X, Y, Z form a separate, disconnected component (try goal = Z).
# ----------------------------------------------------------------------
DEMO_EDGES = [
    ("S", "A", 1), ("S", "B", 5), ("A", "B", 4), ("A", "C", 2),
    ("B", "G", 10), ("B", "F", 2), ("F", "G", 6), ("C", "D", 2),
    ("C", "E", 3), ("D", "G", 3), ("E", "G", 9),
    ("X", "Y", 2), ("Y", "Z", 1),
]

SETTINGS = {"verbose": True, "step": False}



# helpers

def say(msg=""):
    """Print only when verbose (hidden during the silent comparison run)."""
    if SETTINGS["verbose"]:
        print(msg)


def wait():
    """In step mode, wait for Enter after each step."""
    if SETTINGS["verbose"] and SETTINGS["step"]:
        input("   [Press Enter for next step] ")


def fmt_cost(c):
    if isinstance(c, float) and c.is_integer():
        return str(int(c))
    return str(round(c, 2)) if isinstance(c, float) else str(c)


def fmt_nodes(items):
    return "[" + ", ".join(str(i) for i in items) + "]" if items else "[] (empty)"


def fmt_path(path):
    return " -> ".join(path) if path else "(none)"


def path_cost(graph, path):
    return sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1))


# ----------------------------------------------------------------------
# Graph building / display
# ----------------------------------------------------------------------
def build_graph(edges, extra_nodes=(), directed=False):
    """graph = {node: {neighbor: cost}}"""
    graph = {}
    for n in extra_nodes:
        graph.setdefault(n, {})
    for a, b, w in edges:
        graph.setdefault(a, {})
        graph.setdefault(b, {})
        graph[a][b] = min(w, graph[a].get(b, w))
        if not directed:
            graph[b][a] = min(w, graph[b].get(a, w))
    return graph


def print_graph(state):
    graph = state["graph"]
    print("\n" + "=" * 60)
    print("GRAPH BEING SEARCHED  (" + ("directed" if state["directed"] else "undirected") + ", weighted)")
    print("=" * 60)
    print("Adjacency list  node: neighbor(cost), ...   (neighbors visited in alphabetical order)")
    for n in sorted(graph):
        nbrs = ", ".join(f"{m}({fmt_cost(w)})" for m, w in sorted(graph[n].items()))
        print(f"  {n}: {nbrs if nbrs else '(no connections)'}")
    print(f"\nStart node: {state['start']}    Goal node: {state['goal']}")
    print("=" * 60)


# ----------------------------------------------------------------------
# Result container
# ----------------------------------------------------------------------
def make_result(found, path, cost, explored):
    return {"found": found, "path": path, "cost": cost, "explored": explored}


# ----------------------------------------------------------------------
# 1. RANDOM SEARCH 
# ----------------------------------------------------------------------
def random_search(graph, start, goal):
    say("\n>>> RANDOM SEARCH: every step picks a RANDOM node from the frontier.")
    say("    No ordering rule -> results may change on every run (not optimal, not systematic).")
    frontier = [(start, [start], 0)]
    explored = []
    step = 0
    while frontier:
        step += 1
        say(f"\n--- Step {step} ---")
        say(f"Frontier (candidates): {fmt_nodes([f[0] for f in frontier])}")
        idx = random.randrange(len(frontier))
        node, path, cost = frontier.pop(idx)
        explored.append(node)
        say(f"Random choice: candidate #{idx + 1} of {len(frontier) + 1} -> '{node}'  (picked purely by chance)")
        say(f"Current node: {node}   Path so far: {fmt_path(path)}   Cost: {fmt_cost(cost)}")
        if node == goal:
            say(f"GOAL '{goal}' reached!")
            return make_result(True, path, cost, explored)
        waiting = [f[0] for f in frontier]
        for nb, w in sorted(graph[node].items()):
            if nb in explored:
                say(f"   Skip {nb}: already explored")
            elif nb in waiting:
                say(f"   Skip {nb}: already in frontier")
            else:
                frontier.append((nb, path + [nb], cost + w))
                waiting.append(nb)
                say(f"   Add {nb} to frontier (edge cost {fmt_cost(w)})")
        say(f"Explored so far: {fmt_nodes(explored)}")
        wait()
    say("\nFrontier is empty: every reachable node was tried and the goal was not found.")
    return make_result(False, [], 0, explored)


# ----------------------------------------------------------------------
# 2. BFS - FIFO queue
# ----------------------------------------------------------------------
def bfs(graph, start, goal):
    say("\n>>> BFS: uses a QUEUE (first in, first out). Explores ALL nodes at depth k before depth k+1.")
    say("    Finds the path with the FEWEST EDGES (ignores edge costs).")
    queue = deque([(start, [start], 0)])
    seen = {start}
    explored = []
    last_level = -1
    step = 0
    while queue:
        step += 1
        say(f"\n--- Step {step} ---")
        say(f"Queue (front -> back): {fmt_nodes([q[0] for q in queue])}")
        node, path, cost = queue.popleft()
        level = len(path) - 1
        if level != last_level:
            say(f"*** Now exploring LEVEL {level} (nodes {level} edge(s) from the start) ***")
            last_level = level
        explored.append(node)
        say(f"Next node: '{node}' (it was at the FRONT of the queue = waited the longest)")
        say(f"Current node: {node}   Path: {fmt_path(path)}   Cost: {fmt_cost(cost)}")
        if node == goal:
            say(f"GOAL '{goal}' reached at level {level}!")
            return make_result(True, path, cost, explored)
        for nb, w in sorted(graph[node].items()):
            if nb in seen:
                say(f"   Skip {nb}: already discovered")
            else:
                seen.add(nb)
                queue.append((nb, path + [nb], cost + w))
                say(f"   Enqueue {nb} at the BACK (level {level + 1})")
        say(f"Explored so far: {fmt_nodes(explored)}")
        wait()
    say("\nQueue is empty: the goal is not reachable from the start.")
    return make_result(False, [], 0, explored)


# ----------------------------------------------------------------------
# 3. DFS - LIFO stack
# ----------------------------------------------------------------------
def dfs(graph, start, goal):
    say("\n>>> DFS: uses a STACK (last in, first out). Goes as DEEP as possible, then backtracks.")
    say("    Finds A path (not necessarily short or cheap).")
    stack = [(start, [start], 0)]
    explored = []
    prev = None
    step = 0
    while stack:
        step += 1
        say(f"\n--- Step {step} ---")
        say(f"Stack (bottom -> top): {fmt_nodes([s[0] for s in stack])}")
        node, path, cost = stack.pop()
        if node in explored:
            say(f"Popped '{node}' but it was already explored -> ignored")
            wait()
            continue
        if prev is not None and len(path) >= 2 and path[-2] != prev:
            say(f"BACKTRACK: '{prev}' was a dead end, returning to '{path[-2]}' to try another branch")
        elif len(path) >= 2:
            say(f"Going DEEPER: from '{path[-2]}' to '{node}'")
        explored.append(node)
        prev = node
        say(f"Next node: '{node}' (TOP of the stack = most recently added)")
        say(f"Current node: {node}   Depth: {len(path) - 1}   Path: {fmt_path(path)}   Cost: {fmt_cost(cost)}")
        if node == goal:
            say(f"GOAL '{goal}' reached!")
            return make_result(True, path, cost, explored)
        pushed = []
        for nb, w in reversed(sorted(graph[node].items())):  # reversed so alphabetical-first is popped first
            if nb in explored or nb in path:
                say(f"   Skip {nb}: already explored / on current path")
            else:
                stack.append((nb, path + [nb], cost + w))
                pushed.append(nb)
        if pushed:
            say(f"   Pushed {fmt_nodes(list(reversed(pushed)))}; the first of these will be popped next")
        else:
            say("   No new neighbors: dead end")
        say(f"Explored so far: {fmt_nodes(explored)}")
        wait()
    say("\nStack is empty: the goal is not reachable from the start.")
    return make_result(False, [], 0, explored)


# ----------------------------------------------------------------------
# 4. IDS - repeated depth-limited DFS with growing limit
# ----------------------------------------------------------------------
def ids(graph, start, goal):
    say("\n>>> IDS: runs DFS again and again with depth limit 0, 1, 2, ...")
    say("    Memory-light like DFS, fewest-edges like BFS. Nodes get RE-EXPLORED each round.")
    explored = []
    step = 0
    for limit in range(len(graph)):
        say(f"\n{'#' * 8} ROUND: depth limit = {limit} (restart from '{start}') {'#' * 8}")
        stack = [(start, [start], 0)]
        cutoff = False
        round_nodes = []
        while stack:
            step += 1
            say(f"\n--- Step {step} (limit {limit}) ---")
            say(f"Stack (bottom -> top): {fmt_nodes([s[0] for s in stack])}")
            node, path, cost = stack.pop()
            depth = len(path) - 1
            explored.append(node)
            round_nodes.append(node)
            say(f"Next node: '{node}' (top of stack)")
            say(f"Current node: {node}   Depth: {depth}/{limit}   Path: {fmt_path(path)}   Cost: {fmt_cost(cost)}")
            if node == goal:
                say(f"GOAL '{goal}' reached within depth limit {limit}!")
                return make_result(True, path, cost, explored)
            children = [(nb, w) for nb, w in sorted(graph[node].items()) if nb not in path]
            if depth == limit:
                if children:
                    cutoff = True
                    say(f"   Depth limit reached: NOT expanding {fmt_nodes([c[0] for c in children])} (cutoff)")
                else:
                    say("   Depth limit reached, and nothing deeper exists here")
            else:
                for nb, w in reversed(children):
                    stack.append((nb, path + [nb], cost + w))
                say(f"   Pushed {fmt_nodes([c[0] for c in children])}" if children else "   Dead end")
            wait()
        say(f"\nRound {limit} finished without the goal. Nodes visited this round: {fmt_nodes(round_nodes)}")
        if not cutoff:
            say("No cutoff happened: the entire reachable graph was searched. Goal is unreachable.")
            break
        say(f"Cutoff occurred, so deeper nodes exist -> increasing limit to {limit + 1}")
    return make_result(False, [], 0, explored)


# ----------------------------------------------------------------------
# 5. UCS - always expands the cheapest total path cost g(n)
# ----------------------------------------------------------------------
def ucs(graph, start, goal):
    say("\n>>> UCS: always expands the frontier node with the LOWEST TOTAL COST from the start.")
    say("    Finds the CHEAPEST path (may use more edges than BFS).")
    frontier = [(0, start, [start])]
    best = {start: 0}
    closed = set()
    explored = []
    step = 0
    while frontier:
        step += 1
        frontier.sort(key=lambda f: (f[0], f[1]))
        say(f"\n--- Step {step} ---")
        say("Frontier (sorted by cost): " + (", ".join(f"{n}(cost {fmt_cost(c)})" for c, n, _ in frontier)))
        cost, node, path = frontier.pop(0)
        closed.add(node)
        explored.append(node)
        say(f"Next node: '{node}' because it has the LOWEST cost so far ({fmt_cost(cost)})")
        say(f"Current node: {node}   Path: {fmt_path(path)}   Cost: {fmt_cost(cost)}")
        if node == goal:
            say(f"GOAL '{goal}' popped with cost {fmt_cost(cost)} -> guaranteed cheapest!")
            return make_result(True, path, cost, explored)
        for nb, w in sorted(graph[node].items()):
            new = cost + w
            if nb in closed:
                say(f"   Skip {nb}: already finalized with a cheaper/equal cost")
            elif nb not in best:
                best[nb] = new
                frontier.append((new, nb, path + [nb]))
                say(f"   Add {nb}: {fmt_cost(cost)} + {fmt_cost(w)} = {fmt_cost(new)}")
            elif new < best[nb]:
                say(f"   CHEAPER route to {nb}: {fmt_cost(best[nb])} -> {fmt_cost(new)} (via {node}); replacing old entry")
                best[nb] = new
                frontier = [f for f in frontier if f[1] != nb]
                frontier.append((new, nb, path + [nb]))
            else:
                say(f"   Keep old route to {nb}: new cost {fmt_cost(new)} is not better than {fmt_cost(best[nb])}")
        say(f"Explored so far: {fmt_nodes(explored)}")
        wait()
    say("\nFrontier is empty: the goal is not reachable from the start.")
    return make_result(False, [], 0, explored)


ALGORITHMS = {
    1: ("Random Search", random_search),
    2: ("Breadth-First Search (BFS)", bfs),
    3: ("Depth-First Search (DFS)", dfs),
    4: ("Iterative Deepening Search (IDS)", ids),
    5: ("Uniform-Cost Search (UCS)", ucs),
}

NOTES = {
    1: "Not optimal: random choices, results vary per run.",
    2: "Fewest edges guaranteed, but NOT necessarily the cheapest cost.",
    3: "Finds some path; neither shortest nor cheapest.",
    4: "Fewest edges guaranteed (like BFS); repeats work each round.",
    5: "Cheapest cost guaranteed (may use more edges).",
}


# ----------------------------------------------------------------------
# Results display
# ----------------------------------------------------------------------
def print_result(choice, res, state):
    name = ALGORITHMS[choice][0]
    print("\n" + "=" * 60)
    print(f"FINAL RESULT - {name}")
    print("=" * 60)
    print(f"Start: {state['start']}   Goal: {state['goal']}")
    print(f"Goal found     : {'YES' if res['found'] else 'NO (goal unreachable from start)'}")
    if res["found"]:
        print(f"Final path     : {fmt_path(res['path'])}")
        print(f"Edges in path  : {len(res['path']) - 1}")
        print(f"Path cost      : {fmt_cost(res['cost'])}")
    print(f"Nodes explored : {len(res['explored'])} (unique: {len(set(res['explored']))})")
    print(f"Exploration order: {fmt_nodes(res['explored'])}")
    print(f"Note: {NOTES[choice]}")
    print("=" * 60)


def compare_all(state):
    print("\nRunning all algorithms silently on the same graph...")
    SETTINGS["verbose"] = False
    results = {}
    try:
        for k, (_, fn) in ALGORITHMS.items():
            results[k] = fn(state["graph"], state["start"], state["goal"])
    finally:
        SETTINGS["verbose"] = True

    print("\n" + "=" * 78)
    print(f"COMPARISON   start = {state['start']}   goal = {state['goal']}")
    print("=" * 78)
    print(f"{'Algorithm':<34}{'Found':<7}{'Edges':<7}{'Cost':<8}{'Explored':<9}Path")
    print("-" * 78)
    for k, (name, _) in ALGORITHMS.items():
        r = results[k]
        if r["found"]:
            print(f"{name:<34}{'Yes':<7}{len(r['path']) - 1:<7}{fmt_cost(r['cost']):<8}"
                  f"{len(r['explored']):<9}{fmt_path(r['path'])}")
        else:
            print(f"{name:<34}{'No':<7}{'-':<7}{'-':<8}{len(r['explored']):<9}-")
    print("-" * 78)
    found = {k: r for k, r in results.items() if r["found"]}
    if found:
        min_cost = min(r["cost"] for r in found.values())
        min_edges = min(len(r["path"]) - 1 for r in found.values())
        print("Cheapest cost (" + fmt_cost(min_cost) + ") by : " +
              ", ".join(ALGORITHMS[k][0] for k, r in found.items() if r["cost"] == min_cost))
        print(f"Fewest edges ({min_edges}) by : " +
              ", ".join(ALGORITHMS[k][0] for k, r in found.items() if len(r["path"]) - 1 == min_edges))
        print("Tip: Random Search may give a different result on each run; run again to see.")
    else:
        print("No algorithm could reach the goal (it is unreachable from the start).")
    print("=" * 78)


# ----------------------------------------------------------------------
# Input handling
# ----------------------------------------------------------------------
def ask_yes_no(prompt):
    while True:
        a = input(prompt + " (y/n): ").strip().lower()
        if a in ("y", "yes"):
            return True
        if a in ("n", "no"):
            return False
        print("  Please type y or n.")


def ask_node(graph, prompt):
    lookup = {n.lower(): n for n in graph}
    while True:
        raw = input(prompt).strip()
        if raw.lower() in lookup:
            return lookup[raw.lower()]
        print(f"  Invalid node '{raw}'. Available nodes: {', '.join(sorted(graph))}")


def choose_endpoints(state, default_start=None, default_goal=None):
    graph = state["graph"]
    print(f"\nAvailable nodes: {', '.join(sorted(graph))}")
    if default_start and default_goal:
        print(f"(Demo suggestion: start = {default_start}, goal = {default_goal}; "
              f"try goal = Z for an unreachable goal)")
    state["start"] = ask_node(graph, "Enter START node: ")
    state["goal"] = ask_node(graph, "Enter GOAL node : ")
    if state["start"] == state["goal"]:
        print("Note: start and goal are the same node, so every algorithm finishes instantly.")


def build_custom_graph():
    print("\n--- Custom graph entry ---")
    print("Type one edge per line:  node1 node2 cost   (example: A B 4)")
    print("Type a single name to add an isolated node (example: Z)")
    print("Press Enter on an empty line when finished. Costs must be positive numbers.")
    directed = ask_yes_no("Should edges be directed (one-way)?")
    edges, nodes = [], set()
    while True:
        line = input("edge> ").strip()
        if not line:
            if len(nodes) >= 2:
                break
            print("  Enter at least 2 nodes before finishing.")
            continue
        parts = line.split()
        if len(parts) == 1:
            nodes.add(parts[0])
        elif len(parts) == 3:
            try:
                w = float(parts[2])
            except ValueError:
                print("  Invalid cost: must be a number.")
                continue
            if w <= 0:
                print("  Cost must be greater than 0.")
                continue
            w = int(w) if w.is_integer() else w
            edges.append((parts[0], parts[1], w))
            nodes.update(parts[:2])
        else:
            print("  Invalid format. Use: node1 node2 cost")
    return build_graph(edges, nodes, directed), directed


def setup_graph(state):
    print("\nGraph source:")
    print("  1. Built-in demonstration graph")
    print("  2. Enter my own graph")
    while True:
        c = input("Choose 1 or 2: ").strip()
        if c == "1":
            state["graph"] = build_graph(DEMO_EDGES)
            state["directed"] = False
            print_graph({**state, "start": "S", "goal": "G"})
            print("Demo hint: BFS/IDS pick S->B->G (2 edges, cost 15) but UCS picks "
                  "S->A->C->D->G (4 edges, cost 8).")
            choose_endpoints(state, "S", "G")
            return
        if c == "2":
            state["graph"], state["directed"] = build_custom_graph()
            choose_endpoints(state)
            return
        print("  Invalid choice.")


# ----------------------------------------------------------------------
# Menu loop
# ----------------------------------------------------------------------
def print_menu(state):
    print("\n" + "-" * 60)
    print(f"Current: start = {state['start']}, goal = {state['goal']}, "
          f"step mode = {'ON' if SETTINGS['step'] else 'OFF'}")
    print("-" * 60)
    print("1. Random Search")
    print("2. Breadth-First Search (BFS)")
    print("3. Depth-First Search (DFS)")
    print("4. Iterative Deepening Search (IDS)")
    print("5. Uniform-Cost Search (UCS)")
    print("6. Exit")
    print("7. Compare ALL algorithms on this graph")
    print("8. Change start / goal nodes")
    print("9. Change graph (demo or custom)")
    print("10. Show graph again")
    print("11. Toggle step-by-step mode (pause after every step)")


def main():
    print("=" * 60)
    print("   SEARCH ALGORITHM SIMULATOR")
    print("   Random | BFS | DFS | IDS | UCS")
    print("=" * 60)
    state = {"graph": {}, "directed": False, "start": None, "goal": None}
    setup_graph(state)
    SETTINGS["step"] = ask_yes_no("Pause after every step (press Enter to advance)?")

    while True:
        print_menu(state)
        choice = input("Select an option: ").strip()
        if not choice.isdigit():
            print("Invalid input. Please enter a number from the menu.")
            continue
        c = int(choice)
        if c in ALGORITHMS:
            print_graph(state)
            name, fn = ALGORITHMS[c]
            print(f"\nStarting {name} ...")
            res = fn(state["graph"], state["start"], state["goal"])
            print_result(c, res, state)
        elif c == 6:
            print("Goodbye! Happy learning.")
            break
        elif c == 7:
            print_graph(state)
            compare_all(state)
        elif c == 8:
            choose_endpoints(state)
        elif c == 9:
            setup_graph(state)
        elif c == 10:
            print_graph(state)
        elif c == 11:
            SETTINGS["step"] = not SETTINGS["step"]
            print(f"Step-by-step mode is now {'ON' if SETTINGS['step'] else 'OFF'}.")
        else:
            print("Invalid option. Choose a number from the menu.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting simulator. Goodbye!")