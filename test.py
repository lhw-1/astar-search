import cv2
import numpy as np
import os, sys, getopt

from Map import Map

def main(argv):
    
    inputfile = ''
    outputfile = ''
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print('Input file is "', inputfile)
    print('Output file is "', outputfile)

    PATH = './out.npy'
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        im = np.load(PATH)
        map = Map(im, is_np = True)
        astar(map, (0, 600))
    else:
        im = cv2.imread(inputfile, cv2.IMREAD_COLOR)
        map = Map(im, out = outputfile, is_np = False)
        np.save(PATH, map.map)

if __name__ == "__main__":
   main(sys.argv[1:])







