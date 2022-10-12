import numpy as np
import math

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.f = 0
        self.parent = None

    # Returns the resulting node from moving by a given translation
    # The new node's parent is set to this node
    def translate(self, translations):
        new_node = Node(self.x + translations[0], self.y + translations[1])
        new_node.parent = self
        return new_node

    # Calculates the euclidean distance between two given points
    def euclidean_heuristics(self, node):

        # Return the euclidean distance between two cartesian nodes
        return math.sqrt((self.x - node.x)**2 + (self.y - node.y)**2)
    
    def __lt__(self, other):
        return self.f < other.f




