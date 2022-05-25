import numpy as np

from typing import Sequence, Union
from skimage.filters import sobel

from .search import search
from .utilities import preprocess_image
from .cost_calc import StaticExtractor, DynamicExtractor
import json

with open('./config.json', 'r') as f:
    default_params = json.load(f)

class Pathfinder:
    def __init__(self, image: np.array, capacity=None, use_dynamic_features=True):
        """
        Parameters
        ----------
        image : np.array
            array of shape (3, 3, height, width)
        capacity : int
            number of last pixels used for dynamic cost calculation
        """

        image, brightness = preprocess_image(image)
        static_extractor = StaticExtractor()
        static_cost = static_extractor(image, brightness)

        self.static_cost = static_cost.astype(np.int)
        self.maximum_cost = static_extractor.maximum_cost
        self.capacity = capacity or default_params['dynamic']['history_capacity']

        self.current_dynamic_cost = None
        self.dynamic_extractor = DynamicExtractor(image, brightness) if use_dynamic_features else lambda x: None

        self.grads_map = sobel(brightness)
        self.processed_pixels = list()

    def find_path(self, seed_x: int, seed_y: int, free_x: int, free_y: int) -> Sequence[tuple]:
        if len(self.processed_pixels) != 0:
            self.current_dynamic_cost = self.dynamic_extractor(self.processed_pixels)

        free_x, free_y = self.get_cursor_snap_point(free_x, free_y, self.grads_map)
        path = self.calc_segment(
            seed_x, seed_y, free_x, free_y,
            self.maximum_cost, self.current_dynamic_cost, self.static_cost
        )
        self.processed_pixels.extend(reversed(path))
        if len(self.processed_pixels) > self.capacity:
            self.processed_pixels = self.processed_pixels[-self.capacity:]
        return path

    @staticmethod
    def calc_segment(seed_x: int, seed_y: int, free_x: int, free_y: int, maximum_cost: int,
                          dynamic_cost: Union[np.array, None], static_cost: np.array) -> Sequence[tuple]:
        h, w = static_cost.shape[2:]
        if dynamic_cost is None:
            dynamic_cost = np.zeros((3, 3, h, w), dtype=np.int)

        node_map = search(static_cost, dynamic_cost, w, h, seed_x, seed_y, maximum_cost)
        cur_x, cur_y = node_map[:, free_x, free_y]

        history = []
        while (cur_x, cur_y) != (seed_x, seed_y):
            history.append((cur_y, cur_x))
            cur_x, cur_y = node_map[:, cur_x, cur_y]
        return history

    @staticmethod
    def get_cursor_snap_point(x: int, y: int, grads: np.array, snap_scale: int = 3):
        region = grads[y - snap_scale:y + snap_scale, x - snap_scale:x + snap_scale]

        max_grad_idx = np.unravel_index(region.argmax(), region.shape)
        max_grad_idx = np.array(max_grad_idx)
        y, x = max_grad_idx + np.array([y - snap_scale, x - snap_scale])
        return x, y