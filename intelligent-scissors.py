import cv2
import argparse
from src.costs import laplacian_zero_crossing

def get_args():
    parser = argparse.ArgumentParser('intelligent-scissors')
    parser.add_argument('impath', help='image path')
    parser.add_argument('-C')
    return parser.parse_args()

mouse_pos = None
clk_list = []

def click_event_handler(event, x, y, flags, params):
    global mouse_pos, clk_list
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_pos = (x, y)
    if event in [cv2.EVENT_LBUTTONDOWN, cv2.EVENT_RBUTTONDOWN]:
        clk_list.append((x, y))

args = get_args()
image = cv2.imread(args.impath)
print(type(image))
cv2.imshow('image', image)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("image_gray", image)
cv2.imshow('f_Z', laplacian_zero_crossing(image))
cv2.setMouseCallback('image', click_event_handler)
cv2.waitKey()
print(mouse_pos, clk_list)