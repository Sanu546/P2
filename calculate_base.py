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
    assert(linalg.norm(x) != 0)
    
    x_norm = x * 1/linalg.norm(x)
    
    
    
    
    # Build transform matrix from points
    T = [[0,0,0,points[0,0]],
         [0,0,0,points[1,0]],
         [0,0,0,points[2,0]],
         [0,0,0,1],]
    
    print(f"\nResulting transform:\n{x_norm}")
    
calculate_base(points)