import queue
import cv2
import argparse

from cv2 import waitKey

from src.pathfinder import Pathfinder

def get_args():
    parser = argparse.ArgumentParser('intelligent-scissors')
    parser.add_argument('impath', help='image path')
    parser.add_argument('-C')
    return parser.parse_args()

def click_event_handler(event, x, y, flags, params):
    mouse_clicks = params
    # if event == cv2.EVENT_MOUSEMOVE:
    #     mouse_pos.put((x,y))
    if event in [cv2.EVENT_LBUTTONDOWN, cv2.EVENT_RBUTTONDOWN]:
        mouse_clicks.append((x,y))


if __name__ == "__main__":
    # SETUP
    print("Start")
    mouse_clicks = []
    args = get_args()
    image = cv2.imread(args.impath)
    image_temp = image.copy()
    cv2.imshow('image', image)
    cv2.setMouseCallback('image', click_event_handler,mouse_clicks)
    finished = False
    while True:
        if len(mouse_clicks)>0:
            image_temp = cv2.circle(image_temp, mouse_clicks[-1], 1, (255,0,0), 2)
            cv2.imshow('image',image_temp)
        k = cv2.waitKey(1)
        if  k==32 & 0xFF == ord(' '): # Spacja - zatwierdzenie punktów
            finished = True
            break
        if k==113 & 0xFF == ord('q'): # q - wyjście bez zapisywania
            break
    
    cv2.destroyAllWindows()

    if finished:
        print("Processing points")
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        pathfinder = Pathfinder(image_gray)
        path = []
        for i in range(len(mouse_clicks)-1):
            path.extend(pathfinder.find_path(*mouse_clicks[i], *mouse_clicks[i+1]))
        print(path)

        # ----- sumuluję otrzymaną maskę -----------
        # ------------------------------------------

        for x, y in path:
            image_temp[x, y, :] = (255, 255, 0)

        cv2.imshow("output",image_temp)
        cv2.waitKey(0)
        cv2.destroyAllWindows()