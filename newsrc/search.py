import numpy as np
from dataclasses import dataclass
from typing import Tuple, Union

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

class NodesList:
    def __init__(self, w, h):
        self._nodes_dict = {
            (x, y): Node(x=0, y=0, active=False, expanded=False,
                cost_total=0, is_cost_infinite=True) for x in range(w) for y in range(h)}
    
    def node_at(self, x: int, y: int):
        if (x, y) not in self._nodes_dict:
            self._nodes_dict[(x, y)] = Node(x=x, y=y, active=False, expanded=False, cost_total=0, is_cost_infinite=True)
        return self._nodes_dict[(x, y)]
        

def search(static_cost, dynamic_cost, w, h, seed_x, seed_y, max_local_cost):
    nodes_list = NodesList(w, h)
    # nodes_dict = {(x, y): Node(x=seed_x, y=seed_y, active=False, expanded=False, cost_total=0, is_cost_infinite=True) for x in range(w) for y in range(h)}
    # nodes_dict[(seed_x, seed_y)].is_cost_infinite = False
    nodes_list.node_at(seed_x, seed_y).is_cost_infinite = False
    print(nodes_list.node_at(seed_x, seed_y))
    active_list = {i: [] for i in range(max_local_cost)}
    active_list[0].append((seed_x, seed_y))

    num_of_active_lists = 1
    tmp_cost = 0
    last_expanded_cost = 0

    p_x, p_y, q_x, q_y = 0, 0, 0, 0
    x_shift, y_shift = 0, 0

    next_node_map = np.zeros((2, w, h), dtype=np.int)

    shifts = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]

    while num_of_active_lists != 0:
        last_expanded_cost -= 1

        while True:
            last_expanded_cost += 1
            list_index = last_expanded_cost % max_local_cost

            if len(active_list[list_index]) != 0:
                break
        
        p = active_list[list_index].pop()
        p_x, p_y = p
        nodes_list.node_at(p_x, p_y).expanded = True
        last_expanded_cost = nodes_list.node_at(p_x, p_y).cost_total

        if len(active_list[list_index]) == 0:
            num_of_active_lists -= 1
        
        for x_shift, y_shift in shifts:

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
            if nodes_list.node_at(q_x, q_y).expanded:
                continue

            # compute cumulative cost to neighbour
            # TODO fix axes order
            tmp_cost = nodes_list.node_at(p_x, p_y).cost_total + static_cost[y_shift + 1, x_shift + 1, p_y, p_x]
            tmp_cost += dynamic_cost[y_shift + 1, x_shift + 1, p_y, p_x]

            if nodes_list.node_at(q_x, q_y).active:
                if (nodes_list.node_at(q_x, q_y).is_cost_infinite or tmp_cost < nodes_list.node_at(q_x, q_y).cost_total):
                # remove higher cost neighbor
                    list_index = nodes_list.node_at(q_x, q_y).cost_total % max_local_cost
                    active_list[list_index].remove(q)

                    # reduce number of active buckets
                    if len(active_list[list_index]) == 0:
                        num_of_active_lists -= 1

            # if neighbour not in list
            if not nodes_list.node_at(q_x, q_y).active:
                # assign neighbor’s cumulative cost
                nodes_list.node_at(q_x, q_y).cost_total = tmp_cost
                nodes_list.node_at(q_x, q_y).is_cost_infinite = False

                # place node to the active list
                list_index = nodes_list.node_at(q_x, q_y).cost_total % max_local_cost
                active_list[list_index].append(q)

                # set back pointer
                next_node_map[0, q_x, q_y] = p_x
                next_node_map[1, q_x, q_y] = p_y

                # increase number of active buckets
                if len(active_list[list_index]) == 1:
                    num_of_active_lists += 1
    return next_node_map