import numpy as np
from spatialmath import SO3
import spatialmath.base as smb

def matrixToAxisAngle(pose):
    # Extract rotation matrix
    R = SO3([
        [pose[0][0], pose[0][1], pose[0][2]],
        [pose[1][0], pose[1][1], pose[1][2]],
        [pose[2][0], pose[2][1], pose[2][2]]
    ])
    
    angleAxis = R.angvec()
    
    angleAxisVec = angleAxis[0] * angleAxis[1]
    angleAxisVec = np.append([pose[0][3], pose[1][3], pose[2][3]], angleAxisVec)    
    return angleAxisVec

def axisAngleToMatrix(pose):
    theta = np.sqrt(pose[3]**2+pose[4]**2+pose[5]**2)
    k = np.array([pose[3],pose[4],pose[5]])/theta
    
    r1 = np.array([k[0]**2*(1-np.cos(theta))+np.cos(theta),
                    k[0]*k[1]*(1-np.cos(theta))+k[2]*np.sin(theta),
                    k[0]*k[2]*(1-np.cos(theta))-k[1]*np.sin(theta)])
    
    r2 = np.array([k[0]*k[1]*(1-np.cos(theta))-k[2]*np.sin(theta),
                    k[1]**2*(1-np.cos(theta))+np.cos(theta),
                    k[1]*k[2]*(1-np.cos(theta))+k[0]*np.sin(theta)])
    
    r3 = np.array([k[0]*k[2]*(1-np.cos(theta))+k[1]*np.sin(theta),
                    k[1]*k[2]*(1-np.cos(theta))-k[0]*np.sin(theta),
                    k[2]**2*(1-np.cos(theta))+np.cos(theta)])
    
    T = np.array([[r1[0],r2[0],r3[0],pose[0]],
                     [r1[1],r2[1],r3[1],pose[1]],
                     [r1[2],r2[2],r3[2],pose[2]],
                     [0,0,0,1]])
    return np.round(T,6)

def matrixToRPY(pose):
    R = np.array([[pose[0][0],pose[0][1],pose[0][2]],[pose[1][0],pose[1][1],pose[1][2]],[pose[2][0],pose[2][1],pose[2][2]]])
    
    r = np.arctan2(R[2][1],R[2][2])
    p = np.arctan2(-R[2][0],np.sqrt(R[0][0]**2+R[1][0]**2))
    y = np.arctan2(R[1][0],R[0][0])
    
    return [r,p,y,pose[0][3],pose[1][3],pose[2][3]]

def RPYtoRMatrix(pose):
    r = pose[0]
    p = pose[1]
    y = pose[2]
    
    Rx = np.array([[1,0,0],
                    [0,np.cos(r),-np.sin(r)],
                    [0,np.sin(r),np.cos(r)]])
    Ry = np.array([[np.cos(p),0,np.sin(p),],
                    [0,1,0],
                    [-np.sin(p),0,np.cos(p)]])
    Rz = np.array([[np.cos(y),-np.sin(y),0],
                    [np.sin(y),np.cos(y),0],
                    [0,0,1]])
    
    R = Rz @ Ry @ Rx
    
    return R

# matrix = np.array([[-1.00000000e+00, -1.00000000e-06,  0.00000000e+00,5.07500101e-02],
#        [-1.00000000e-06,  9.06308000e-01, -4.22618000e-01, -2.96883397e-01],
#        [ 1.00000000e-06, -4.22618000e-01, -9.06308000e-01, 9.73039785e-02],
#        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 1.00000000e+00]])

# acMatrix = [[    -1.000000,    -0.000000,     0.000000,    50.551742],
#      [-0.000000,     1.000000,    -0.000000,  -296.844405 ],
#      [-0.000000,    -0.000000,    -1.000000,    97.231132 ],
#       [0.000000,     0.000000,     0.000000,     1.000000 ]
# ]

# urPos = matrixToAxisAngle(matrix)
# print(urPos, "urPos")
# print(np.degrees(rpy), "rpy")
# print(urPos, "urPos")



# ur5pos = [-.288579832,  -.582838966,   .495898987,    -0.103287,    -2.100478,    -0.110654]

# ur5pos = axisAngleToMatrix(ur5pos)

# print(ur5pos)

# matrix = matrixToRPY(ur5pos)

# print(matrix)
# matrix = np.array([[matrix[0][0],matrix[0][1],matrix[0][2],0],
#                     [matrix[1][0],matrix[1][1],matrix[1][2],0],
#                     [matrix[2][0],matrix[2][1],matrix[2][2],0],
#                     [0,0,0,1]])
# print(matrix)
# print(matrixToRPY(matrix))