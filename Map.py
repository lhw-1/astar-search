import cv2
import numpy as np

from Node import Node
from utils import convert_to_pixel

# Threshold for how close a point can be to an obstacle at any given time
OBS_THRESHOLD = 10

class Map:
    def __init__(self, image):
        self.map = self.convert_bw(image)

    # Converts any image to monochrome
    def convert_bw(self, image):
        self.height, self.width, self.channel = image.shape

        new_image = np.zeros((self.height, self.width, self.channel))
        for i in range(self.height):
            for j in range(self.width):
                color_avg = np.sum(image[i][j]) / 3
                new_image[i][j] = [0, 0, 0] if color_avg < 128 else [255, 255, 255]

        return new_image
    
    # Add padding to the current map
    def add_padding(self, padding):
        self.padding = padding
        prev_height = self.height
        prev_width = self.width
        self.height = self.height + padding
        self.width = self.width + padding

        new_map = np.zeros((self.height, self.width, self.channel))
        for i in range(self.height):
            for j in range(self.width):
                if i < padding or i > padding + prev_height or j < padding or j > padding + prev_width:
                    new_map[i][j] = [255, 255, 255]
                else:
                    new_map[i][j] = self.map[i - padding][j - padding]
        
        self.map = new_map

    def valid(self, node):
        node_pixel = convert_to_pixel((node.x, node.y), self.height, self.width, self.padding)

        # Check if the perimeter of OBS_THRESHOLD around the given node is valid
        for i in range(OBS_THRESHOLD * 2 + 1):
            for j in range(OBS_THRESHOLD * 2 + 1):
                
                # If there is an obstacle pixel, return False
                if self.map[i + node_pixel[1] - OBS_THRESHOLD][j + node_pixel[0] - OBS_THRESHOLD][0] == 0:
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




