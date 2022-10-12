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
GOAL_THRESHOLD = 5

def astar(map, goal, start = (0, 0)):

    # Initialise the Starting node
    start_node = Node(start[0], start[1])
    start_node.set_g(0)
    start_node.set_f(0)

    # Initialise the Goal node
    goal_node = Node(goal[0], goal[1])

    # Initialise the Open List and the Closed List
    open_list = []
    closed_list = []

    # Set possible translations for successor generation
    translations = [
        (1,0), # East
        (1,-1), # South-East
        (0,-1), # South
        (-1,-1), # South-West
        (-1,0), # West
        (-1,1), # North-West
        (0,1), # North
        (1,1) # North-East
    ]

    # Convert Open List into a Heap
    heapq.heapify(open_list)
    heapq.heapify(closed_list)

    # Put the starting node into the Open List
    # All nodes will be the following format: (f-value, x-coord, y-coord)
    heapq.heappush(open_list, start_node)

    # Conditional Loop while the Open list is not empty
    goal_found = False
    while(len(open_list) > 0 and not goal_found):

        # Find the node with the lowest f-value in the Open List
        current_node = heapq.heappop(open_list)

        # Generate successors
        for i in range(len(translations)):
            successor_node = current_node.translate(translations[i])

            # If successor == goal, stop search
            if goal_node.euclidean_heuristics(successor_node) < GOAL_THRESHOLD:
                goal_found = True
                break
            
            # Else, compute g and h for successor
            else:
                # successor.g = q.g + distance between q and successor
                dist = euclidean_distance((current_node.x, current_node.y), (successor_node.x, successor_node.y))
                successor_node.set_g(current_node.g + dist)

                # successor.h = distance from goal to successor
                successor_h = goal_node.euclidean_heuristics(successor_node)

                # successor.f = successor.g + successor.h
                successor_node.set_f(successor_node.g + successor_h)
            
            # By default, first_condition is set to True
            # This is in the case where open_list is empty, and so trivially there are no nodes with same position and lower f than successor
            first_condition = True

            # By default, second_condition is set to True
            # This is in the case where closed_list is empty, and so trivially there are no nodes with same position and lower f than successor
            second_condition = True

            for i in range(len(open_list)):

                # If a node with the same position as successor is in the Open List 
                # with a lower f than successor, skip this successor
                first_condition = not (open_list[i].x == successor_node.x and open_list[i].y == successor_node.y and open_list[i].f < successor_node.f)

            for i in range(len(closed_list)):

                # If a node with the same position as successor is in the Closed List 
                # with a lower f than successor, skip this successor
                second_condition = not (closed_list[i].x == successor_node.x and closed_list[i].y == successor_node.y and closed_list[i].f < successor_node.f)


            # If the successor is not in a valid position
            # skip this successor
            third_condition = map.valid(successor_node)

            # Otherwise, add the node to the open list
            if first_condition and second_condition and third_condition:
                heapq.heappush(open_list, successor_node)
    
        # Push current_node on the Closed List
        heapq.heappush(closed_list, current_node)
        print(current_node.x, current_node.y)
    
    # Closed List now contains the optimal route from start to goal
    for i in range(len(closed_list)):
        map.set_valid(closed_list[i])
    
    map.set_special(start_node)
    map.set_special(goal_node)

    # Return map
    cv2.imwrite("out.png", map.map)

# im = cv2.imread("./test.png", cv2.IMREAD_COLOR)

im = np.zeros((200, 200, 3))
im.fill(255)
map = Map(im)
map.add_padding(20)
# Note: padding should be sufficiently large so that checking for validity will succeed for non-visible areas
# According to assumption that area outside bounds are assumed to be traversable by default

astar(map, (50, 50))
