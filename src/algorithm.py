from typing import Tuple, Callable
import numpy as np
from time import sleep
from costs import *

class GraphPath:
    pass

class LiveWire2D_Solver:
    def __init__(self, image: np.ndarray, cost_func: Callable = None) -> None:
        self.image = image
        self.cost_matrix = np.full(self.image.shape, np.inf) # macierz kosztow
        self.processed_matrix = np.full(self.image.shape, False) # macierz przetworzonych pikseli
        self.active_pixels = np.full(self.image.shape, False)

        self.lzc = laplacian_zero_crossing(image)
        self.gm = 1 - gradient(image)[0]
        # self.cost_func = cost_func
    
    def __get_pixel_neighbours(self, pixel):
        pixel_y, pixel_x = pixel
        if len(self.image.shape) == 3:
            size_y, size_x, _ = self.image.shape
        elif len(self.image.shape) == 2:
            size_y, size_x = self.image.shape
        output = []

        for x, y in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            neighbouring_pixel_x = pixel_x + x
            neighbouring_pixel_y = pixel_y + y
            if 0 <= neighbouring_pixel_x < size_x:
                if 0 <= neighbouring_pixel_y < size_y:
                    output.append((neighbouring_pixel_y, neighbouring_pixel_x))
        
        return output

    def solve(self, start_pixel: Tuple, cost_func: Callable): #TUTAJ
        # setup start pixel
        self.active_pixels[start_pixel] = True #Czy nie potrzeba zresetować?
        self.cost_matrix[start_pixel] = 0
        output = {}
        # while there are pixels to consider
        while not np.all(self.active_pixels == False):

            # get valid pixels cost
            valid_pixels_matrix = np.full(self.image.shape, np.inf)
            valid_pixels_matrix[self.active_pixels == True] = 1
            print(self.cost_matrix)
            print(valid_pixels_matrix)
            active_cost_matrix = np.multiply(self.cost_matrix, valid_pixels_matrix)
            active_cost_matrix[np.isnan(active_cost_matrix)] = np.inf

            curr_pixel = np.unravel_index(np.argmin(active_cost_matrix, axis=None), active_cost_matrix.shape)

            self.active_pixels[curr_pixel] = False
            self.processed_matrix[curr_pixel] = True
            curr_pixel_neighbourhood = self.__get_pixel_neighbours(curr_pixel)
            for neighbour in curr_pixel_neighbourhood:
                if not self.processed_matrix[neighbour]:
                    temp_cost = cost_func(curr_pixel, neighbour)
                    if self.active_pixels[neighbour]:
                        if temp_cost < self.cost_matrix[neighbour]:
                            self.active_pixels[neighbour] = False
                    if not self.active_pixels[neighbour]:
                        self.cost_matrix[neighbour] = temp_cost
                        output[neighbour] = curr_pixel
                        self.active_pixels[neighbour] = True
        return output


if __name__ == '__main__':
    image = np.zeros((5, 3))
    solver = LiveWire2D_Solver(image)
    out = solver.solve((4, 2), calc_pixel_local_cost)
    print(out)
    print(solver.cost_matrix)

