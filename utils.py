import math

# Converts the given node = (pix_y, pix_x) to cartesian values (cart_x, cart_y)
# Bottom center of image (minus padding) is set as the origin
# The precise location of each pixel is assumed to be the center of the square pixel
# Width and Height is inclusive of padding, and assumes that padding is equal on all four sides
def convert_to_cartesian(node, height, width, padding):

    # Origin is located at:
    origin = ((width - 1) / 2, height - padding - 0.5)

    # node = (pix_y, pix_x)
    pix_y = node[0]
    pix_x = node[1]

    # Calculate cartesian mapping against the origin
    cart_x = pix_x - origin[0]
    cart_y = origin[1] - pix_y

    return (cart_x, cart_y)

def convert_to_pixel(node, height, width, padding):

    # Origin is located at:
    origin = ((width - 1) / 2, height - padding - 0.5)

    # node = (pix_x, pix_y)
    cart_x = node[0]
    cart_y = node[1]

    # Calculate cartesian mapping against the origin
    pix_x = round(cart_x + origin[0])
    pix_y = round(origin[1] - cart_y)

    return (pix_y, pix_x)

# General euclidean distance between two points
def euclidean_distance(point_1, point_2):
    return math.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)



