import sys
from rtde_stuff.rtde_com import RTDEConnection
import time
import numpy as np
from gui.P2_GUI import MainWindow
import vision.objRec as objRec
from frames import Pose
from typing import List


UR5 = RTDEConnection() # Connnect to the UR5 robot

cellSpacingX = 0.1 # The spacing between the cells in the x direction
cellSpacingY = 0.1 # The spacing between the cells in the y direction

# The frame for the ramp
rampFrame = Pose(np.array([[    -0.787945,    -0.321117,     0.525382,   .223402945 ],
     [-0.610211,     0.521369,    -0.596504,  -.461119440 ],
     [-0.082371,    -0.790606,    -0.606759,   .464068150 ],
      [0.000000,     0.000000,     0.000000,     1.000000 ]]

    ))

cellFrames: List[Pose] = [] # The frames for the cells

def exampleProgram():
    UR5.moveJoint([np.radians(-41.62), np.radians(-66.38), np.radians(-110.76), np.radians(56.17), np.radians(93.86), np.radians(38.53)]) # Move to a specific position
    UR5.moveTCP([0.29, -0.25, 0.50, 0.02, 2.8, -1.362]) # Move to a specific position
    print("Move added to queue")
    UR5.moveTCPandWait([0.40, -0.55, 0.20, 0.50, 1.5, -1.362], "l") # Move to a specific position
    print(f"Moved to final position({str(UR5.getCurrentPos())})")
    UR5.setToolPos(50)
    time.sleep(2)

def pickUpCells():
    print("Picking up cells")
    UR5.moveTCP(rampFrame.getApproach())
    UR5.moveTCPandWait(rampFrame.getGlobalPos(), "l")
    print(UR5.getCurrentPos())
    return
    for cell in cellFrames:
        if cell.isEmpty:
            continue
        UR5.moveTCP(cell.getApproach())
        UR5.moveTCP(cell.getGlobalPos(), "l")
        cell.isEmpty = True
        UR5.moveTCP(cell.getApproach(), "l")
        
def generateCellFrames():
    for i in range(4):  
        for j in range(2):
            cellFrames.append(Pose(np.array([[    1,     0,     0,   i*cellSpacingX ],
            [0,     1,     0,   j*cellSpacingY ],
            [0,     0,     1,   0 ],
            [0,     0,     0,     1 ]]), rampFrame, isCell = True, color = "blue"))

def main():
    window = MainWindow()
    generateCellFrames()
    window.controlMenu.testMenu.setFunctionNext(pickUpCells) # Set the function to be called when the button is pressed
    colors = objRec.get_colors() # Get the colors of the cells 
    
    window.cellDisplay.update_colors(colors) # Set the colors of the cells
    window.runUI() # Run the GUI
    
#stuff so you can ctrl+c to exit the program
try:
    main()
    
except KeyboardInterrupt:
    print("Disconnected from robot")
    UR5.kill()
    sys.exit()





