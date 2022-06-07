import numpy as np
import heapq


def get_path(graph, start, end, cost_vh, cost_diag):
    q = [(0, start, ())]  # Heap of (cost, path_head, path_rest).
    visited = set()       # Visited vertices.
    while True:
        (cost, v1, path) = heapq.heappop(q)
        if v1 not in visited:
            visited.add(v1)
            if v1 == end:
                return list(path)[::-1] + [v1]
            path = (v1, *path)
            for (v2, cost2) in graph[v1].items():
                if v2 not in visited:

                    v1_y, v1_x = v1
                    v2_y, v2_x = v2

                    y_shift = v2_y - v1_y
                    x_shift = v2_x - v1_x

                    if v1_x == v2_x or v1_y == v2_y:
                        total_cost = cost + cost_vh[y_shift + 1, x_shift + 1, v1_y, v1_x]
                    else:
                        total_cost = cost + cost_diag[y_shift + 1, x_shift + 1, v1_y, v1_x]
                    heapq.heappush(q, (total_cost, v2, path))
