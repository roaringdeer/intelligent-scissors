import numpy as np
import json
import scipy
from skimage.filters import gaussian, laplace, sobel_h, sobel_v
from .utilities import unfold, create_spatial_feats, flatten_first_dims


class CostEvaluator:
    def __init__(self, laplace_kernels=None, laplace_weights=None, std=None,
                 laplace_w=None, direction_w=None, magnitude_w=None, maximum_cost=None, config_file='./config.json'):

        with open(config_file, 'r') as f:
            config_params = json.load(f)

        std = std or config_params['gaussian_kernel']
        laplace_w = laplace_w or config_params['laplace_w']
        direction_w = direction_w or config_params['direction_w']
        magnitude_w = magnitude_w or config_params['magnitude_w']
        maximum_cost = maximum_cost or config_params['maximum_cost']

        self.std = std
        self.maximum_cost = maximum_cost
        self.laplace_w = laplace_w * maximum_cost
        self.direction_w = direction_w * maximum_cost
        self.magnitude_w = magnitude_w * maximum_cost

        self.laplace_weights = laplace_weights or config_params['laplace_weights']
        self.laplace_kernels = laplace_kernels or config_params['laplace_kernels']

        assert len(self.laplace_weights) == len(self.laplace_kernels), \
            "Sequences must have equal length."

    def __call__(self, image: np.array, brightness: np.array) -> np.array:
        # calculate laplace cost
        l_cost = self.get_laplace_cost(image)
        l_cost = unfold(l_cost)
        l_cost = np.ceil(self.laplace_w * l_cost)
        # calculate direction costs
        d_cost = self.get_direction_cost(brightness)
        d_cost = np.ceil(self.direction_w * d_cost)
        m_diag_cost, _ = self.gradient(image)
        m_vh_cost = m_diag_cost/np.sqrt(2)
        m_diag_cost = np.ceil(self.magnitude_w * m_diag_cost)
        m_vh_cost = np.ceil(self.magnitude_w * m_vh_cost)
        # calculate total static cost
        total_cost = np.squeeze(l_cost + d_cost + m_vh_cost)
        total_diag_cost = np.squeeze(l_cost + d_cost + m_diag_cost)
        return total_cost, total_diag_cost

    def get_laplace_cost(self, image: np.array) -> np.array:
        n_channels, *shape = image.shape
        total_cost = np.zeros((n_channels,) + tuple(shape))

        # smooth image
        image = gaussian(image, self.std)
        # calculate zero crossings for each kernel and channel
        for i, channel in enumerate(image):
            for laplace_kernel, w in zip(self.laplace_kernels, self.laplace_weights):
                total_cost[i] = w * self.calculate_single_laplace_cost(channel, laplace_kernel)

        # maximize over the channels
        total_cost = np.max(total_cost, axis=0, keepdims=True)
        return total_cost

    @staticmethod
    def calculate_single_laplace_cost(image: np.array, laplace_kernel_sz: int) -> np.array:
        laplace_map = laplace(image, ksize=laplace_kernel_sz)
        laplace_map = laplace_map[None]
        # create map of neighbouring pixels costs
        cost_map = unfold(laplace_map)
        cost_map = flatten_first_dims(np.squeeze(cost_map))
        # leave only direct neighbours
        cost_map = cost_map[[1, 3, 5, 7], :, :]
        # get max elements with the opposite sign
        signs = np.sign(laplace_map)
        opposites = cost_map * (cost_map * signs < 0)
        opposites = np.max(np.abs(opposites), axis=0)
        output = np.abs(laplace_map) > opposites
        return output

    @staticmethod
    def get_direction_cost(image: np.array, eps=1e-6) -> np.array:
        # calculate vectors perpendicular to gradients
        grads = np.stack([sobel_v(image), -sobel_h(image)])
        grads /= (np.linalg.norm(grads, axis=0) + eps)

        unfolded_grads = unfold(grads)
        grads = grads[:, None, None, ...]

        # calculate dot products
        spatial_feats = create_spatial_feats(image.shape)
        link_feats = np.einsum('i..., i...', spatial_feats, grads)
        # get d_p features
        local_feats = np.abs(link_feats)
        # get d_q features
        sign_mask = np.sign(link_feats)
        distant_feats = sign_mask * np.einsum('i..., i...', spatial_feats, unfolded_grads)
        # calculate total gradient direction cost
        total_cost = 2 / (3 * np.pi) * (np.arccos(local_feats) + np.arccos(distant_feats))
        return total_cost

    @staticmethod
    def gradient(image):
        dx = scipy.ndimage.filters.convolve1d(np.int32(image), np.array([-1, 0, 1]), 1)
        dy = scipy.ndimage.filters.convolve1d(np.int32(image), np.array([-1, 0, 1]), 0)

        grad = np.sqrt(dx**2 + dy**2)
        grad = 1 - grad/np.amax(grad)
        orientation = np.vstack(([dy.T], [-dx.T])).T
        # orientation = (dy, -dx)
        return grad, orientation
    
    # Gradient Magnitude
    def get_magnitude_cost(gradient, p, q):
        if p[0] == q[0] or p[1] == q[1]:
            return gradient[q[0]][q[1]]/np.sqrt(2)
        else: 
            return gradient[q[0]][q[1]]
