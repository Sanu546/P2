import numpy as np
from numpy import linalg
from numpy import pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

points = [[22.8,  15.3, 0],
          [126.7, 51.5, 0],
          [-1.5,  96.7, 30]]

def calculate_base(points):
    
    # Convert to numpy array
    points = np.array(points)
    
    # Print the input
    print(f"\nInput points\n{points}")
    
    # Calculate and normalize x vector
    x = points[1] - points[0]
    assert linalg.norm(x) != 0, "\n\nOrigo and x is the same point!!!\n"
    
    # Norm x, using ord=2 assures that the direction of x is maintained when normalizing
    x_norm = x * 1 / linalg.norm(x, ord=2)
    
    # Project vector from origo to y onto vector x to make it ortogonal with x
    # Calculate and normalize y vector
    y = points[2] - points[0]
    assert linalg.norm(y) != 0, "\n\nOrigo and y is the same point!!!\n"
    
    # Calculate projection of y onto x
    y_orth = y - (np.dot(y,x) / np.dot(x,x)) * x
    #linalg.norm(x, ord=2)
    # Norm y, using ord=2 assures that the direction of y is maintained when normalizing
    y_norm = y_orth * 1 / linalg.norm(y_orth, ord=2)

    
    #Calculate the last vector z which is orthogonal on x and y and therefore can be found by their cross product
    z_norm = np.cross(x_norm,y_norm)
    
    # Final assersions
    assert np.isclose(linalg.norm(x_norm, ord=2), 1, 0.00001) or np.isclose(linalg.norm(x_norm, ord=2), -1, 0.00001), f"\n\nLength of x_norm is {linalg.norm(x_norm, ord=2)} which is not 1 or -1\n"
    assert np.isclose(linalg.norm(y_norm, ord=2), 1, 0.00001) or np.isclose(linalg.norm(y_norm, ord=2), -1, 0.00001), f"\n\nLength of y_norm is {linalg.norm(y_norm, ord=2)} which is not 1 or -1\n"
    assert np.isclose(linalg.norm(z_norm, ord=2), 1, 0.00001) or np.isclose(linalg.norm(z_norm, ord=2), -1, 0.00001), f"\n\nLength of z_norm is {linalg.norm(z_norm, ord=2)} which is not 1 or -1\n"
    
    assert np.isclose(np.dot(x_norm,y_norm), 0, 0.00001), f"\n\nx_norm and y_norm are not orthogonal their dot product is {np.dot(x_norm,y_norm)} which is not 0\n"
    assert np.isclose(np.dot(x_norm,z_norm), 0, 0.00001), f"\n\nx_norm and z_norm are not orthogonal their dot product is {np.dot(x_norm,z_norm)} which is not 0\n"

    # Build transform matrix from points
    base = np.array([x_norm, y_norm, z_norm, points[0]]).T
    base = np.vstack([base, [0,0,0,1]])
        
    print(f"\nResulting transform:\n{base}")
    
    plot_points_and_transforms(points, [base,  np.array([[1,0,0,1],
                                                        [0,1,0,1],
                                                        [0,0,1,1],
                                                        [0,0,0,1]])])


def plot_points_and_transforms(points, transforms):
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the points
    points = np.array(points)
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='b', marker='o', label='Points')
    
    # Plot the transforms
    for transform in transforms:
        # Extract the translation part (last column of the transformation matrix)
        origin = transform[:3, 3]
        
        # Extract the rotation part (first 3 columns of the transformation matrix)
        x_axis = transform[:3, 0]
        y_axis = transform[:3, 1]
        z_axis = transform[:3, 2]
        
        # Plot the origin of the transform
        ax.scatter(origin[0], origin[1], origin[2], c='r', marker='x', label='Transform Origin' if not 'origin_plotted' in locals() else "")
        origin_plotted = True
        
        # Plot the axes of the transform
        ax.quiver(origin[0], origin[1], origin[2], x_axis[0], x_axis[1], x_axis[2], color='r', length=100.0, normalize=True, label='X Axis' if not 'x_axis_plotted' in locals() else "")
        ax.quiver(origin[0], origin[1], origin[2], y_axis[0], y_axis[1], y_axis[2], color='g', length=100.0, normalize=True, label='Y Axis' if not 'y_axis_plotted' in locals() else "")
        ax.quiver(origin[0], origin[1], origin[2], z_axis[0], z_axis[1], z_axis[2], color='b', length=100.0, normalize=True, label='Z Axis' if not 'z_axis_plotted' in locals() else "")
        x_axis_plotted = True
        y_axis_plotted = True
        z_axis_plotted = True
    
    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Set limits (optional, adjust as needed)
    ax.set_xlim([-1000, 1000])
    ax.set_ylim([-1000, 1000])
    ax.set_zlim([-1000, 1000])
    
    # Show legend
    ax.legend()
    
    # Show the plot
    plt.show()


calculate_base(points)