# astar-search
A* Search Algorithm, implemented in Python 3.

## Usage

Simply clone this repository to start testing out the python scripts.

The command to run this script is as such:

`python3 test.py -i [INPUT FILE PATH] -o [OUTPUT FILE PATH] -x [CARTESIAN X-COORDINATE OF GOAL] -y [CARTESIAN Y-COORDINATE OF GOAL]`

E.g.

`python3 test.py -i input.png -o output.png -x 0 -y 600`

This will create an output.png that will contain the path generated.

### Tweakable Parameters 

As this code was meant to be used for a [specific project](https://github.com/lhw-1/rgbd-pathfinder-ros), the algorithm process and the parameters have been pre-set according to our project specifications. The image is converted to a grid map with a Cartesian co-ordinate system, whose origin is considered to be at the center-bottom of the image prior to adding the padding, i.e. for a given image, the origin is located at ((width - 1) / 2, height - padding - 0.5). Regardless, by tweaking some of the parameters (including the starting point of the algorithm), the algorithm can be generalized without issues.

First, in `Map.py`, there are three parameters: `OBS_THRESHOLD`, `PADDING`, and `DIM_RESIZE`. 

`OBS_THRESHOLD` is essentially the minimum distance (in pixels) from any obstacle (or wall) to the optimal path calculated - for example, if you set this value to 0, the path may end up hugging the walls or the obstacles. On the other hand, if this value is set to 5, then all nodes in the path will be at least 5 pixels away from any obstacles and/or walls. It is recommended to set it to a value that would allow an agent to comfortably avoid the obstacles while ensuring that a path can still be found. 

`PADDING` is the number of white pixels added to all four sides of the image. This was added as an assumption that an unseen environment is traversable without any obstacles, and is specific to the abovementioned project; the value may be set to 0 if this assumption is not necessary.

`DIM_RESIZE` is simply the dimensions that the image will be resized to.

Next, in `astar.py`, there are three parameters: `GOAL_THRESHOLD`, `STEP`, and `START`.

`GOAL_THRESHOLD` is essentially the minimum distance (in pixels) that the end of the path can be from the given goal. The larger the value, the less strict the conditions for reaching the goal will be. Setting this to 0 will mean that the algorithm will try to find a path that can reach the exact values of the given goal coordinates.

`STEP` is the distance (in pixels) between each node, and `START` is the starting point (in cartesian values).
