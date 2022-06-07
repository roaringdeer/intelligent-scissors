from typing import Sequence
import numpy as np
from .search import get_path
from .utilities import preprocess_image
from .cost_evaluator import CostEvaluator

class Pathfinder:
    def __init__(self, image: np.array, config_file: str = './config.json'):
        image, brightness = preprocess_image(image)
        self.image = image
        cost_evaluator = CostEvaluator(config_file=config_file)
        static_cost, static_cost_diag = cost_evaluator(image, brightness)
        self.static_cost = static_cost.astype(np.int)
        self.static_cost_diag = static_cost_diag.astype(np.int)

    def find_path(self, seed_x: int, seed_y: int, free_x: int, free_y: int) -> Sequence[tuple]:
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
        path = get_path(graph, (seed_y, seed_x), (free_y, free_x), self.static_cost, self.static_cost_diag)
        return path
