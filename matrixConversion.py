import numpy as np

def matrixToAxisAngle(pose):
    R = np.array([[pose[0][0],pose[0][1],pose[0][2]],[pose[1][0],pose[1][1],pose[1][2]],[pose[2][0],pose[2][1],pose[2][2]]])
    
    theta = np.arccos((R[0][0]+R[1][1]+R[2][2]-1)/2)
    
    k = (1/(2*np.sin(theta))*np.array([R[1][2]-R[2][1],R[2][0]-R[0][2],R[0][1]-R[1][0]]))
    ku = 1/np.sqrt(k[0]**2+k[1]**2+k[2]**2)*k
    
    return [pose[0][3],pose[1][3],pose[2][3],ku[0]*theta,ku[1]*theta,ku[2]*theta]

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
    
    T = np.array([[r1[0],r1[1],r1[2],pose[0]],
                     [r2[0],r2[1],r2[2],pose[1]],
                     [r3[0],r3[1],r3[2],pose[2]],
                     [0,0,0,1]])
    return round(T,6)

def matrixToRPY(pose):
    R = np.array([[pose[0][0],pose[0][1],pose[0][2]],[pose[1][0],pose[1][1],pose[1][2]],[pose[2][0],pose[2][1],pose[2][2]]])
    
    r = np.arctan2(R[2][1],R[2][2])
    p = np.arctan2(-R[2][0],np.sqrt(R[0][0]**2+R[1][0]**2))
    y = np.arctan2(R[1][0],R[0][0])
    
    return [np.degrees(r),np.degrees(p),np.degrees(y),pose[0][3],pose[1][3],pose[2][3]]

