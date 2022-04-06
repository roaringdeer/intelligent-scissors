from typing import Tuple, Callable
import numpy as np

class GraphPath:
    pass

class LiveWire2D_Solver:
    def __init__(self, image: np.ndarray) -> None:
        self.image = image

    def solve(start_pixel: Tuple, cost_func: Callable) -> GraphPath:
        pass

def get_pixel_neighbours(pixel):
    pass

def algo(start_pixel: Tuple, cost_func: Callable):
    active_pixels = [] # list of active pixels sorted by total cost
    neighbourhood_q = {}
    processed = {}
    g = {}

    g[start_pixel] = 0
    active_pixels.append(start_pixel)

    # while not len(active_pixels) == 0:
    #     for 