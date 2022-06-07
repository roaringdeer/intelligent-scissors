from typing import List, Sequence, Tuple
import numpy as np
import heapq
from .utilities import preprocess_image
from .cost_evaluator import CostEvaluator

class Pathfinder:
    def __init__(self, image: np.array, config_file: str = './config.json'):
        image, brightness = preprocess_image(image)
        self.image = image
        self._create_graph_from_image()
        
        cost_evaluator = CostEvaluator(config_file=config_file)
        cost_vh, cost_diag = cost_evaluator(image, brightness)
        self.cost_vh = cost_vh.astype(np.int)
        self.cost_diag = cost_diag.astype(np.int)
    
    def _create_graph_from_image(self) -> None:
        graph = {}
        _, rows, cols = self.image.shape
        for col in range(cols):
            for row in range(rows):
                neighbors = []
                shifts = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
                for x_shift, y_shift in shifts:
                    if row == 0 and y_shift == -1:
                        continue
                    elif row == rows - 1 and y_shift == 1:
                        continue
                    if col == 0 and x_shift == -1:
                        continue
                    elif col == cols-1 and x_shift == 1:
                        continue
                    neighbors.append((row+y_shift, col+x_shift))
                dist = {n: np.infty for n in neighbors}
                graph[(row,col)] = dist
        self.graph = graph

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        priority_heap = [(0, start, ())]
        visited = set()
        while True:
            cost, p, path = heapq.heappop(priority_heap)
            if p not in visited:
                visited.add(p)
                if p == end:
                    return list(path)[::-1] + [p]
                path = (p, *path)
                for q, _ in self.graph[p].items():
                    if q not in visited:

                        p_y, p_x = p
                        q_y, q_x = q

                        y_shift = q_y - p_y
                        x_shift = q_x - p_x

                        if p_x == q_x or p_y == q_y:
                            total_cost = cost + self.cost_vh[y_shift + 1, x_shift + 1, p_y, p_x]
                        else:
                            total_cost = cost + self.cost_diag[y_shift + 1, x_shift + 1, p_y, p_x]
                        heapq.heappush(priority_heap, (total_cost, q, path))