import numpy as np
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Node:
    x: int
    y: int
    active: bool
    expanded: bool
    cost_total: int
    is_cost_infinite: bool
    prev_node_xy: Tuple[int, int] = None
    next_node_xy: Tuple[int, int] = None

def search(static_cost, dynamic_cost, w, h, seed_x, seed_y, max_local_cost):
    nodes_dict = {(x, y): Node(x=seed_x, y=seed_y, active=False, expanded=False, cost_total=0, is_cost_infinite=True) for x in range(w) for y in range(h)}
    nodes_dict[(seed_x, seed_y)].is_cost_infinite = False
    active_list = {i: [] for i in range(max_local_cost)}
    active_list[0].append((seed_x, seed_y))

    num_of_active_lists = 1
    tmp_cost = 0
    last_expanded_cost = 0

    p_x, p_y, q_x, q_y = 0, 0, 0, 0
    x_shift, y_shift = 0, 0

    next_node_map = np.zeros((2, w, h), dtype=np.int)

    x_shifts = [-1, 0, 1, -1, 1, -1, 0, 1]
    y_shifts = [-1, -1, -1, 0, 0, 1, 1, 1]

    while num_of_active_lists != 0:
        last_expanded_cost -= 1

        while True:
            last_expanded_cost += 1
            list_index = last_expanded_cost % max_local_cost

            if len(active_list[list_index]) != 0:
                break
        
        p = active_list[list_index].pop()
        p_x, p_y = p
        nodes_dict[p].expanded = True
        last_expanded_cost = nodes_dict[p].cost_total

        if len(active_list[list_index]) == 0:
            num_of_active_lists -= 1
        
        for i in range(8):
            x_shift = x_shifts[i]
            y_shift = y_shifts[i]

            if p_y == 0 and y_shift == -1:
                continue
            elif p_y == h - 1 and y_shift == 1:
                continue

            if p_x == 0 and x_shift == -1:
                continue
            elif p_x == w-1 and x_shift == 1:
                continue

            q_x = p_x + x_shift
            q_y = p_y + y_shift
            q = (q_x, q_y)

            # such that not expanded
            if nodes_dict[q].expanded:
                continue

            # compute cumulative cost to neighbour
            # TODO fix axes order
            tmp_cost = nodes_dict[p].cost_total + static_cost[y_shift + 1, x_shift + 1, p_y, p_x]
            tmp_cost += dynamic_cost[y_shift + 1, x_shift + 1, p_y, p_x]

            if nodes_dict[q].active and (nodes_dict[q].is_cost_infinite or tmp_cost < nodes_dict[q].cost_total):
                # remove higher cost neighbor
                list_index = nodes_dict[q].cost_total % max_local_cost
                active_list[list_index].remove(q)

                 # reduce number of active buckets
                if len(active_list[list_index]) == 0:
                    num_of_active_lists -= 1

            # if neighbour not in list
            if not nodes_dict[q].active:
                # assign neighbor’s cumulative cost
                nodes_dict[q].cost_total = tmp_cost
                nodes_dict[q].is_cost_infinite = False

                # place node to the active list
                list_index = nodes_dict[q].cost_total % max_local_cost
                active_list[list_index].append(q)

                # set back pointer
                next_node_map[0, q_x, q_y] = p_x
                next_node_map[1, q_x, q_y] = p_y

                # increase number of active buckets
                if len(active_list[list_index]) == 1:
                    num_of_active_lists += 1
    return next_node_map