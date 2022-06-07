from pathlib import Path
import cv2
import argparse
import timeit

from src.pathfinder import Pathfinder

def get_args():
    parser = argparse.ArgumentParser('intelligent-scissors')
    parser.add_argument('impath', help='image path')
    return parser.parse_args()


if __name__ == "__main__":
    print("Start")
    # mouse_clicks = [(420, 113), (506, 8)]
    # mouse_clicks = [(0, 80), (40, 0)]
    mouse_clicks = [(19, 41), (54, 50), (24,64), (19, 41)]
    args = get_args()
    image = cv2.imread(args.impath)
    data_path = Path("./data")
    configs_path = data_path / Path("./configs")
    images_path = data_path / Path("./images")
    paths_path = data_path / Path("./paths")
    times_file = data_path / Path("./times.txt")
    images_path.mkdir(exist_ok=True)
    paths_path.mkdir(exist_ok=True)
    times_str = ""
    for config_file in configs_path.glob("*.json"):
        
        image_temp = image.copy()
        cfg_num = config_file.stem.split("_")[1]
        
        print(f"Processing points for {config_file}")

        pathfinder = Pathfinder(image)

        path = []
        for i in range(len(mouse_clicks)-1):
            start_xy = mouse_clicks[i]
            end_xy = mouse_clicks[i+1]
            t_start = timeit.default_timer()
            found_path = pathfinder.find_path(*start_xy, *end_xy)
            t_end = timeit.default_timer()
            times_str += f"{cfg_num};{start_xy};{end_xy};{t_end-t_start}\n"
            path.extend(found_path)

        path_str = ""
        for x, y in path:
            image_temp[x, y, :] = (255, 255, 0)
            path_str += f"{x},{y}\n"
        
        pathfile = paths_path / f"path_{cfg_num}.txt"
        pathfile.write_text(path_str)

        cv2.imwrite(str(images_path / f"img_{cfg_num}.jpg"), image_temp)
    times_file.write_text(times_str)

            
        

        