import cv2
import heapq
import math
import numpy as np

from Map import Map
from Node import Node
from utils import euclidean_distance

'''
A Star Search Algorithm

* There must be a wall_threshold (Agent must not go too near the wall)

Each node has g, h, and f.

g = The movement cost to move from starting point to a given point on the grid, following the path generated so far to get there.
h = Estimated movement cost to move from the given square on the grid to the final destination.
(Euclidean heuristics is used here)
f = g + h

1. Initialize the Open List
2. Initialize the Closed List
3. Put the starting node on the Open list (leave f as 0)
4. While Open List is not empty,
   a) Find node with lowest f value on the Open List (call it q)
   b) Pop q off the Open List
   c) Generate q's 8 successors and set their parents to q
   d) For each successor:
      i) If successor == goal, stop search
      ii) Else, compute g and h for successor
          successor.g = q.g + dist between successor and q
          successor.h = Some heuristic
          (Manhattan, Diagonal, or Euclidean)
      iii) Compute f = g + h for successor
      iv) If a node with same position as successor is in the Open List with a lower f than successor, skip this successor
      v) If a node with the same position as successor is in the Closed List with a lower f than successor, skip this successor
         v)i) Else add node to the Open List
   e) Push q on the Closed List
   End
'''

# Threshold for how close a point can be to the goal before it is declared to have reached the goal
# This is measured in pixels, not cartesian values (though it should be synonymous for now)
GOAL_THRESHOLD = 10

# Number of pixels moved per each step
# The bigger the number, the faster the search, but may be less detailed
# If too big, it may fail due to obstacle collisions
# In this case, try setting OBS_THRESHOLD in Map.py to a lower value
STEP = 20

# Starting node
START = (0, 0)

def astar(map, goal, start = START):

    # Initialise the Starting node
    start_node = Node(start[0], start[1])
    start_node.g = 0
    start_node.f = (0)

    # Initialise the Goal node
    # Note that give goal must be in cartesian, not pixel, values
    goal_node = Node(goal[0], goal[1])

    # Initialise the Open List and the Closed List, as well as corresponding Dictionaries
    open_list = []
    closed_list = []
    open_dict = {}
    closed_dict = {}

    # Set possible translations for successor generation
    translations = [
        (STEP,0), # East
        (STEP,-STEP), # South-East
        (0,-STEP), # South
        (-STEP,-STEP), # South-West
        (-STEP,0), # West
        (-STEP,STEP), # North-West
        (0,STEP), # North
        (STEP,STEP) # North-East
    ]

    # Convert Open List into a Heap
    heapq.heapify(open_list)
    heapq.heapify(closed_list)

    # Put the starting node into the Open List
    # All nodes will be the following format: (f-value, x-coord, y-coord)
    heapq.heappush(open_list, start_node)

    # Conditional Loop while the Open list is not empty
    goal_found = False
    found_goal_node = None
    while(len(open_list) > 0 and not goal_found):

        # Find the node with the lowest f-value in the Open List
        current_node = heapq.heappop(open_list)
        print("NODE:",current_node.x, current_node.y)

        # Generate successors
        for i in range(len(translations)):
            successor_node = current_node.translate(translations[i])

            # If successor == goal, stop search
            if goal_node.euclidean_heuristics(successor_node) < GOAL_THRESHOLD:
                goal_found = True
                found_goal_node = successor_node
                print("GOAL FOUND!")
                print("GOAL:", successor_node.x, successor_node.y)
                break
            
            # Else, compute g and h for successor
            else:
                # successor.g = q.g + distance between q and successor
                dist = euclidean_distance((current_node.x, current_node.y), (successor_node.x, successor_node.y))
                successor_node.g = (current_node.g + dist)

                # successor.h = distance from goal to successor
                successor_h = goal_node.euclidean_heuristics(successor_node)

                # successor.f = successor.g + successor.h
                successor_node.f = (successor_node.g + successor_h)

            # If a node with the same position as successor is in the Open List 
            # with a lower f than successor, skip this successor
            if (successor_node.x, successor_node.y) in open_dict:
                first_condition = open_dict[(successor_node.x, successor_node.y)].f < successor_node.f
            else:
                first_condition = True

            # If a node with the same position as successor is in the Closed List 
            # with a lower f than successor, skip this successor
            if (successor_node.x, successor_node.y) in closed_dict:
                second_condition = closed_dict[(successor_node.x, successor_node.y)].f < successor_node.f
            else:
                second_condition = True

            # If the successor is not in a valid position
            # skip this successor
            third_condition = map.valid(successor_node)

            # Otherwise, add the node to the open list
            if first_condition and second_condition and third_condition:
                heapq.heappush(open_list, successor_node)
                open_dict[(successor_node.x, successor_node.y)] = successor_node
    
        # Push current_node on the Closed List
        heapq.heappush(closed_list, current_node)
        closed_dict[(current_node.x, current_node.y)] = current_node
    
    # Trace the optimal route
    valid_node = found_goal_node
    while (not valid_node is None):
        print("VALID:", valid_node.x, valid_node.y)
        map.set_valid(valid_node)
        valid_node = valid_node.parent
    
    map.set_special(start_node)
    map.set_special(goal_node)

    # Return map
    cv2.imwrite(map.out, map.map)
