import numpy as np
from numpy import linalg
from numpy import pi

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


calculate_base(points)