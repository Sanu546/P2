import numpy as np
import matrixConversion as mc

class Pose:
    def __init__(self, id, name, matrix, description, base=None, approach=0.05, isCell=False, color=None ) :
        self.name = name
        self.isCell = isCell
        self.matrix = matrix
        self.base = base
        self.id = id
        self.description = description
        self.approach = np.array([[1,0,0,0],
                                 [0,1,0,0],
                                 [0,0,1,-approach],
                                 [0,0,0,1]])
        
        if not self.isCell:
            return
        
        if color == "grey":
            self.isEmpty = True
        elif color == "red":
            self.isEmpty = False
            self.replace = True
        elif color == "blue":
            self.isEmpty = False
            self.replace = False
        else:
            print("Invalid color")
        
    def getGlobalPos(self):
        if self.base != None:
            return self.base.getGlobalPos() @ self.matrix
        else:
            return self.matrix
        
    def getApproach(self):
        return self.getGlobalPos() @ self.approach
