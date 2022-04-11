import cv2
import argparse
from src.costs import *
from src.algorithm import  *
from multiprocessing import Process, shared_memory

def get_args():
    parser = argparse.ArgumentParser('intelligent-scissors')
    parser.add_argument('impath', help='image path')
    parser.add_argument('-C')
    return parser.parse_args()

mouse_pos = None

def click_event_handler(event, x, y, flags, params):
    clk_list = shared_memory.ShareableList(name='clk_list')
    mouse_pos = shared_memory.ShareableList(name='mouse_pos')
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_pos[0] = x
        mouse_pos[1] = y
    if event in [cv2.EVENT_LBUTTONDOWN, cv2.EVENT_RBUTTONDOWN]:
        i = clk_list.index(-1)
        clk_list[i] = x
        clk_list[i+1] = y

def image_show_process(image):
    clk_list = shared_memory.ShareableList(name='clk_list')
    mouse_pos = shared_memory.ShareableList(name='mouse_pos')
    cv2.imshow('image', image)
    # make clk_list shared with counting process
    cv2.setMouseCallback('image', click_event_handler)
    cv2.waitKey()
    print(mouse_pos, clk_list)
    # image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("image_gray", image_gray)

def find_path():
    clk_list = shared_memory.ShareableList(name='clk_list')
    mouse_pos = shared_memory.ShareableList(name='mouse_pos')
    # obliczenia, algorytm

if __name__ == "__main__":
    # SETUP
    args = get_args()
    image = cv2.imread(args.impath)
    print(type(image))
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('f_Z', laplacian_zero_crossing(image_gray))
    clk_list_shm = shared_memory.ShareableList([-1 for i in range(100)], name='clk_list')
    mouse_pos = shared_memory.ShareableList([0, 0], name='mouse_pos')

    # uruchomienie procesu z obrazem i procesu z poszukiwaniem ścieżki
    image_process = Process(target=image_show_process, args=(image,))
    path_process = Process(target=find_path)
    image_process.start()
    image_process.join() # Czeka z zamknięciem głównego procesu, aż joinowane procesy się zakończą
    cv2.waitKey()