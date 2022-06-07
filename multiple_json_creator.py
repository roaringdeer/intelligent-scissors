import json, os
from pathlib import Path
import numpy as np

def get_json(json_name, laplace, direction, magnitude):
    jsondict = {
        "laplace_w": laplace,
        "direction_w": direction,
        "magnitude_w": magnitude,
        "local": 0.1,
        "inner": 0.1,
        "outer": 0.1,
        "laplace_kernels": [3, 5, 7],
        "gaussian_kernel": 5,
        "laplace_weights": [0.2, 0.3, 0.5],
        "maximum_cost": 255,
        "snap_scale": 3
    }

    with open(json_name, 'w+') as f:
        json.dump(jsondict, f, indent=4)

if __name__ == "__main__":
    data_path = Path("./data")
    configs_path = data_path / Path("configs")
    data_path.mkdir(exist_ok=True)
    configs_path.mkdir(exist_ok=True)
    cfg_num = 0
    for laplace in np.arange(0, 1, 0.1):
        for direction in np.arange(0, 1, 0.1):
            for magnitude in np.arange(0, 1, 0.1):
                get_json(configs_path / f"cfg_{cfg_num}.json", laplace, direction, magnitude)
                cfg_num += 1