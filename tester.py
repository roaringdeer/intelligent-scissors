from pathlib import Path
import cv2
import argparse
import timeit

import numpy as np
cv2.LineSegmentDetector

from src.pathfinder import Pathfinder
from src.utilities import eval_path

def get_args():
    parser = argparse.ArgumentParser('intelligent-scissors')
    parser.add_argument('impath', help='image path')
    return parser.parse_args()


if __name__ == "__main__":
    print("Start")
    # mouse_clicks = [(420, 113), (506, 8)]
    # mouse_clicks = [(0, 80), (40, 0)]
    path_reference = cv2.imread("testimage3_path_reference.png")
    mouse_clicks = [(19, 41), (54, 50), (24,64), (19, 41)]
    args = get_args()
    image = cv2.imread(args.impath)

    data_dir = Path("./data")
    configs_dir = data_dir / Path("./configs")
    images_dir = data_dir / Path("./images")
    paths_txt_dir = data_dir / Path("./paths_txt")
    paths_img_dir = data_dir / Path("./paths_img")
    
    times_file = data_dir / Path("./times.txt")
    summary_file = data_dir / Path("./summary.txt")

    images_dir.mkdir(exist_ok=True)
    paths_txt_dir.mkdir(exist_ok=True)
    paths_img_dir.mkdir(exist_ok=True)
    
    times_str = "cfg_num;start_xy;end_xy;exec_time\n"
    summary_str = "cfg_num;path_score;time_total\n"
    for config_file in configs_dir.glob("*.json"):
        
        image_temp = image.copy()
        path_image = np.zeros_like(image)
        cfg_num = config_file.stem.split("_")[1]
        
        print(f"Processing points for {config_file}")

        pathfinder = Pathfinder(image, config_file=config_file)

        path = []
        time_total = 0
        for i in range(len(mouse_clicks)-1):
            start_xy = mouse_clicks[i]
            end_xy = mouse_clicks[i+1]
            t_start = timeit.default_timer()
            found_path = pathfinder.find_path(*start_xy, *end_xy)
            t_end = timeit.default_timer()
            exec_time = t_end - t_start
            times_str += f"{cfg_num};{start_xy};{end_xy};{exec_time}\n"
            time_total += exec_time
            path.extend(found_path)

        path_str = ""
        for x, y in path:
            image_temp[x, y, :] = (255, 255, 0)
            path_image[x, y, :] = (255, 255, 255)
            path_str += f"{x},{y}\n"
        pathfile = paths_txt_dir / f"path_{cfg_num}.txt"
        pathfile.write_text(path_str)

        # cv2.imwrite(str(images_dir / f"img_{cfg_num}.png"), image_temp)
        # cv2.imwrite(str(paths_img_dir / f"path_{cfg_num}.png"), path_image)
        
        path_score, hits, misses = eval_path(path_image, path_reference)
        summary_str += f"{cfg_num};{path_score};{time_total}\n"
        print(f"Path score (misses/hits+misses): {path_score}, hits: {hits}, misses: {misses}")

        # cv2.imshow("reference", path_reference)
        # cv2.waitKey(0)
        print("=" * 10)
    times_file.write_text(times_str)
    summary_file.write_text(summary_str)

            
        

        