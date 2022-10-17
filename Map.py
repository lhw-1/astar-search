import cv2
import numpy as np
import random

from Node import Node
from utils import convert_to_pixel

# Threshold for how close a point can be to an obstacle at any given time
OBS_THRESHOLD = 5

# The value for the padding around the image
# Note: padding should be sufficiently large so that checking for validity will succeed for non-visible areas
# According to assumption that area outside bounds are assumed to be traversable by default
PADDING = 50

# Dimensions for Resizing
DIM_RESIZE = (400, 400)

class Map:
    def __init__(self, image, out = "output.png", is_np = False):

        image_resize = self.resize(image)
        self.height, self.width, self.channel = image_resize.shape
        self.padding = PADDING
        self.out = out

        if is_np:
            self.map = image_resize
        else:
            self.map = self.convert_bw(image_resize)
            self.add_padding(self.padding)
            cv2.imwrite("map.png", self.map)
    
    # Resize image
    def resize(self, image):
        return cv2.resize(image, DIM_RESIZE, interpolation = cv2.INTER_AREA)

    # Converts any image to monochrome
    def convert_bw(self, image):
        new_image = np.zeros((self.height, self.width, self.channel))
        for i in range(self.height):
            for j in range(self.width):
                color_avg = np.sum(image[i][j]) / 3
                new_image[i][j] = [0, 0, 0] if color_avg < 128 else [255, 255, 255]

        return new_image
    
    # Add padding to the current map
    def add_padding(self, padding):
        prev_height = self.height
        prev_width = self.width
        self.height = self.height + (2 * padding)
        self.width = self.width + (2 * padding)

        new_map = np.zeros((self.height, self.width, self.channel))
        for i in range(self.height):
            for j in range(self.width):
                if i < padding or i > padding + prev_height or j < padding or j > padding + prev_width:
                    new_map[i][j] = [255, 255, 255]
                else:
                    new_map[i][j] = self.map[i - 1 - padding][j - 1 - padding]
        
        self.map = new_map

    def valid(self, node):
        node_pixel = convert_to_pixel((node.x, node.y), self.height, self.width, self.padding)

        # Check if the perimeter of OBS_THRESHOLD around the given node is valid
        for i in range(OBS_THRESHOLD * 2 + 1):
            for j in range(OBS_THRESHOLD * 2 + 1):
                
                # If there is an obstacle pixel, return False
                # If you have reached the ends of the map, also return False
                if i + node_pixel[1] - OBS_THRESHOLD >= self.width or j + node_pixel[0] - OBS_THRESHOLD >= self.height or self.map[j + node_pixel[0] - OBS_THRESHOLD][i + node_pixel[1] - OBS_THRESHOLD][0] == 0:
                    print("MAP SHAPE", self.map.shape, "VALID CHECK", node_pixel)
                    return False
        
        # Else return True
        return True
        
    def set_valid(self, node):
        node_pixel = convert_to_pixel((node.x, node.y), self.height, self.width, self.padding)

        new_map = self.map
        new_map[node_pixel[0]][node_pixel[1]] = [255, 0, 0]
        self.map = new_map
        
    def set_special(self, node):
        node_pixel = convert_to_pixel((node.x, node.y), self.height, self.width, self.padding)

        new_map = self.map
        new_map[node_pixel[0]][node_pixel[1]] = [0, 0, 255]
        self.map = new_map




