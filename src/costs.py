import cv2
import numpy as np

def scaled_gradient():
    pass

def h(pixel):
    pass


def laplacian_zero_crossing2(image):
    laplacian_kernel = np.array(([0, 1, 0], [1, -4, 1], [0, 1, 0]), dtype="int")
    laplacianed_image = cv2.filter2D(image, -1, laplacian_kernel)
    z_c_image = np.zeros(laplacianed_image.shape)

    for i in range(0,laplacianed_image.shape[0]-1):
        for j in range(0,laplacianed_image.shape[1]-1):
            if laplacianed_image[i][j]>0:
                if laplacianed_image[i+1][j] < 0 or laplacianed_image[i+1][j+1] < 0 or laplacianed_image[i][j+1] < 0:
                    z_c_image[i,j] = 1
            elif laplacianed_image[i][j] < 0:
                if laplacianed_image[i+1][j] > 0 or laplacianed_image[i+1][j+1] > 0 or laplacianed_image[i][j+1] > 0:
                    z_c_image[i,j] = 1
    return z_c_image


def sobel_zero_crossing(image):
    sobel_x = cv2.Sobel(image,cv2.CV_64F,1,0,ksize=3)
    sobel_y = cv2.Sobel(image,cv2.CV_64F,0,1,ksize=3)
    sobel_first_derivative = cv2.magnitude(sobel_x,sobel_y)
    sobel_test = np.empty_like (sobel_first_derivative)
    sobel_test[:] = sobel_first_derivative


def laplacian_zero_crossing(image):
    kernel = np.array([[-1, -1, -1],[-1, 8, -1],[-1, -1, -1]])
    image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    newimage = np.zeros_like(image)

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            if image[x, y].all(0):
                newimage[x, y] = 255
            else:
                newimage[x, y] = 0
    # new_image = np.array
    # ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)
    return newimage

# Laplacian Zero-Crossing
def f_Z(pixel):
    pass

# Gradient Direction
def f_D(pixel, neighbour_pixel):
    pass

# Gradient Magnitude
def f_G(pixel):
    pass

def calc_pixel_local_cost(pixel, neighbour_pixel, w_Z: float = 0.43, w_D: float = 0.43, w_G: float = 0.14):
    """
    Executes calculation: w_Z*f_Z + w_D*f_D + w_G*f_G
    """
    # return w_Z*f_Z(pixel) + w_D*f_D(pixel, neighbour_pixel) + w_G*f_G(pixel)
    return 1 # pixel[0] + pixel[1] + neighbour_pixel[0] + neighbour_pixel[1]