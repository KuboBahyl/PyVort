import properties
from scipy import interpolate
import numpy as np

def spline3D(segments, item, next_item, type):
    knots = 4

    if (type=="nearest"):
        first_item = properties.go_backward(segments, item)
        next_next_item = properties.go_forward(segments, next_item)

    elif (type=="every_second"):
        first_item = properties.go_backward(segments, properties.go_backward(segments, item))
        next_next_item = properties.go_forward(segments, properties.go_forward(segments, next_item))

    coords_to_spline=[first_item['coords'],
                      item['coords'],
                      next_item['coords'],
                      next_next_item['coords']]

    x_to_spline = [coord[0] for coord in coords_to_spline]
    y_to_spline = [coord[1] for coord in coords_to_spline]
    z_to_spline = [coord[2] for coord in coords_to_spline]

    tck, u = interpolate.splprep([x_to_spline,y_to_spline,z_to_spline], s=2)
    true_points = 11 # num of new virtual points
    u_fine = np.linspace(0,1,true_points)
    x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

    return np.array([x_fine[5], y_fine[5], z_fine[5]])
