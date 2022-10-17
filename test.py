import cv2
import numpy as np
import os, sys, getopt

from Map import Map
from Node import Node
from astar import astar

def main(argv):
    
    inputfile = ''
    outputfile = ''
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:x:y:",["ifile=","ofile=","xcoord=", "ycoord="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile> -x <xcoord> -y <ycoord>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile> -x <xcoord> -y <ycoord>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-x", "--xcoord"):
            xcoord = arg
        elif opt in ("-y", "--ycoord"):
            ycoord = arg

    print('Input file is ', inputfile)
    print('Output file is ', outputfile)
    print('X-coordinate is ', xcoord)
    print('Y-coordinate is ', ycoord)

    PATH = './' + outputfile + '.npy'
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        im = np.load(PATH)
        map = Map(im, out = outputfile, is_np = True)
        valid = map.valid(Node(int(xcoord), int(ycoord)))
        print("VALID GOAL" if valid else "INVALID GOAL")
        if valid:
            astar(map, (int(xcoord), int(ycoord)))
        else:
            print("EXITING...")
    else:
        im = cv2.imread(inputfile, cv2.IMREAD_COLOR)
        map = Map(im, out = outputfile, is_np = False)
        np.save(PATH, map.map)
        im = np.load(PATH)
        map = Map(im, out = outputfile, is_np = True)
        valid = map.valid(Node(int(xcoord), int(ycoord)))
        print("VALID GOAL" if valid else "INVALID GOAL")
        if valid:
            astar(map, (int(xcoord), int(ycoord)))
        else:
            print("EXITING...")

if __name__ == "__main__":
   main(sys.argv[1:])







