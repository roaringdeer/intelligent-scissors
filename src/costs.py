import cv2
import numpy as np
import scipy.ndimage

def gradient(image):
    dx = scipy.ndimage.filters.convolve1d(np.int32(image), np.array([-1, 0, 1]), 1)
    dy = scipy.ndimage.filters.convolve1d(np.int32(image), np.array([-1, 0, 1]), 0)

    grad = np.sqrt(dx**2 + dy**2)
    grad = grad/np.amax(grad)
    orientation = (dy, -dx)
    return grad, orientation


def laplacian_zero_crossing(image):
    kernel = np.array([[0, -1, 0],[-1, 4, -1],[0, -1, 0]])
    image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    #newimage = np.zeros_like(image)
    ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)
    return image

# Laplacian Zero-Crossing
def f_Z(pixel, lzc):
    return lzc[pixel[0]][pixel[1]]


# Gradient Direction
def f_D(pixel, neighbour_pixel):
    pass


# Gradient Magnitude
def f_G(gradient, p, q):
    if p[0] == q[0] or p[1] == q[1]:
        return gradient[q[0]][q[1]]/np.sqrt(2)
    else: 
        return gradient[q[0]][q[1]]


def calc_pixel_local_cost(pixel, neighbour_pixel, gradient, lzc, w_Z: float = 0.43, w_D: float = 0.43, w_G: float = 0.14):
    """
    Executes calculation: w_Z*f_Z + w_D*f_D + w_G*f_G
    """
    # return w_Z*f_Z(pixel, lzc) + w_D*f_D(pixel, neighbour_pixel) + w_G*f_G(gradient, pixel, neighbour_pixel)
    return 1 # pixel[0] + pixel[1] + neighbour_pixel[0] + neighbour_pixel[1]


if __name__ == "__main__":
    image = cv2.imread("Lena.png")
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imL = laplacian_zero_crossing(image_gray)
    imG = G(image_gray)
    #imD = f_D(image_gray)
    cv2.imshow("L", imL)
    cv2.imshow("G", imG)
    #cv2.imshow("D", imD)
    cv2.waitKey()
    cv2.destroyAllWindows()