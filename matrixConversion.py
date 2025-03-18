import numpy as np

def matrixToAxisAngle(pose):
    R = np.array([[pose[0][0],pose[0][1],pose[0][2]],[pose[1][0],pose[1][1],pose[1][2]],[pose[2][0],pose[2][1],pose[2][2]]])
    theta = np.arccos((R[0][0]*R[1][1]*R[2][2]-1)/2)
    k = (1/(2*np.sin(theta))*np.array([R[2][1]-R[1][2],R[0][2]-R[2][0],R[1][0]-R[0][1]]))
    ku = 1/np.sqrt(k[0]**2+k[1]**2+k[2]**2)*k
    return [pose[0][3],pose[1][3],pose[2][3],ku[0]*theta,ku[1]*theta,ku[2]*theta]
    

T = np.array([[    -0.000000,     0.000000,     1.000000,   474.500000 ],
     [-1.000000,    -0.000000,    -0.000000,  -109.300000 ],
      [0.000000,    -1.000000,     0.000000,   608.950000 ],
      [0.000000,     0.000000,     0.000000,     1.000000 ]])

axisAngle = matrixToAxisAngle(T)
print(axisAngle)