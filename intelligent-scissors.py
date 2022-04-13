import queue
import cv2
import argparse

from cv2 import waitKey
from src.costs import *
from src.algorithm import  *
from multiprocessing import Process, shared_memory, Queue

def get_args():
    parser = argparse.ArgumentParser('intelligent-scissors')
    parser.add_argument('impath', help='image path')
    parser.add_argument('-C')
    return parser.parse_args()

mouse_pos = None

def click_event_handler(event, x, y, flags, params):
    clk_list = params[0]
    mouse_pos = params[1]
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_pos.put((x,y))
    if event in [cv2.EVENT_LBUTTONDOWN, cv2.EVENT_RBUTTONDOWN]:
        clk_list.put((x,y))

def image_show_process(image, clk_q, mouse_pos_q, image_shape):
    print("Image process starting")
    cv2.imshow('image', image)
    cv2.setMouseCallback('image', click_event_handler,(clk_q, mouse_pos_q))
    path_shm = shared_memory.SharedMemory(name='PATH_SHM')
    path_array = np.ndarray(image_shape, dtype = np.uint8, buffer = path_shm.buf) 

    while True:
        # rysowanie po obrazie

        if cv2.waitKey(32) & 0xFF == ord(' '):
            break #przerwanie pętli po wciasnieciu q

    mouse_pos_q.put(-1) # Kończy pętle w find_path

def find_path(clk_q, mouse_pos_q, image_shape):
    print("Find path process starting")
    clk_list = []
    mouse_pos = (0,0)
    path_shm = shared_memory.SharedMemory(name='PATH_SHM')
    path_array = np.ndarray(image_shape, dtype = np.uint8, buffer = path_shm.buf) 
    while mouse_pos!=-1: # do zmiany na jakiś lepszy warunek?
        try:
            mouse_pos = mouse_pos_q.get() # czeka aż będzie w kolejce coś do wyjęcia - myszka się ruszy
            clk_list.append(clk_q.get_nowait()) # czy w kolejce coś do wyjęcia, bez czekania
        except queue.Empty:
            continue # kolejka clk_q pusta, nic się nie dzieje
        # obliczenia, algorytm
    print(mouse_pos, clk_list)

if __name__ == "__main__":
    # SETUP
    print("Start")
    args = get_args()
    clk_q = Queue()
    mouse_pos_q = Queue()
    image = cv2.imread(args.impath)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    path_shm = shared_memory.SharedMemory(create=True, size=image_gray.size*8, name='PATH_SHM') #Rozmiaru obrazu, array na ścieżkę
    #cv2.imshow('f_Z', laplacian_zero_crossing(image_gray))
    # uruchomienie procesu z obrazem i procesu z poszukiwaniem ścieżki
    image_process = Process(target=image_show_process, args=(image, clk_q, mouse_pos_q, image_gray.shape, ))
    path_process = Process(target=find_path, args=(clk_q, mouse_pos_q, image_gray.shape, ))
    image_process.start()
    path_process.start()
    image_process.join() # Czeka z zamknięciem głównego procesu, aż joinowane procesy się zakończą
    cv2.waitKey()