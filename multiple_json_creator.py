import json, os
from pathlib import Path
import numpy as np

def get_json(json_name, laplace, direction, magnitude):
    jsondict = {
        "laplace_w": laplace,
        "direction_w": direction,
        "magnitude_w": magnitude,
        "laplace_kernels": [3, 5, 7],
        "gaussian_kernel": 5,
        "laplace_weights": [0.2, 0.3, 0.5],
        "maximum_cost": 255,
    }

    with open(json_name, 'w+') as f:
        json.dump(jsondict, f, indent=4)

if __name__ == "__main__":

    limit_up = 5
    limit_down = 0
    step = 0.3

    data_path = Path("./data")
    configs_path = data_path / Path("configs")
    data_path.mkdir(exist_ok=True)
    configs_path.mkdir(exist_ok=True)
    cfg_num = 0
    for laplace in np.arange(limit_down, limit_up, step):
        for direction in np.arange(limit_down, limit_up, step):
            for magnitude in np.arange(limit_down, limit_up, step):
                get_json(configs_path / f"cfg_{cfg_num:05}.json", laplace, direction, magnitude)
                cfg_num += 1
    print(f"Created {cfg_num} configurations!")