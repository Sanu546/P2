import sys
from rtde_stuff.rtde_com import RTDEConnection
import time
import numpy as np
from gui.P2_GUI import MainWindow
import vision.objRec as objRec
from frames import Pose
from typing import List


UR5 = RTDEConnection() # Connnect to the UR5 robot

moves = [] # The moves that the robot will make

cellSpacingX = 0.1 # The spacing between the cells in the x direction
cellSpacingY = 0.1 # The spacing between the cells in the y direction

currentMove = 0


# The frame for the ramp
rampFrame = Pose(np.array([[    -0.999673,    -0.024494,     0.007347,   .201236369], 
     [-0.023483,     0.765548,    -0.642950,  -.657846558],
      [0.010124,    -0.642913,    -0.765873,   .283486816],
      [0.000000,     0.000000,     0.000000,     1.000000 ]]
))

cellFrames: List[Pose] = [] # The frames for the cells

dropOffFrame = Pose(np.array([[1, 0, 0, 0.5],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]]), rampFrame) # The frame for the drop off location
        
def generateCellFrames():
    for i in range(4):  
        for j in range(2):
            cellFrames.append(Pose(np.array([[    1,     0,     0,   j*cellSpacingX ],
            [0,     1,     0,   i*cellSpacingY ],
            [0,     0,     1,   0 ],
            [0,     0,     0,     1 ]]), rampFrame, isCell = True, color = "blue"))

def generateMoves():
    for cell in cellFrames:
        if cell.isEmpty:
            continue
        moves.append({"move": cell.getApproach(), "type": "j"})
        moves.append({"move": cell.getGlobalPos(), "type": "l"})
        moves.append({"move": cell.getApproach(), "type": "l"})
        moves.append({"move": dropOffFrame.getApproach(), "type": "j"})
        moves.append({"move": dropOffFrame.getGlobalPos(), "type": "l"})
        moves.append({"move": dropOffFrame.getApproach(), "type": "l"})

def runAutoRobot():
    status = UR5.getStatus()
    movesLeft = len(UR5.getAllTargets())

    if movesLeft != 0 and status == "running":
        print("Robot is already running")
        return
    
    if movesLeft !=0 and status == "idle":
        UR5.resume()
        return
    
    for move in moves:
        UR5.moveTCP(move["move"], move["type"])
        
def stopAutoRobot():
    UR5.stop()  

def priorMove():
    global currentMove
    moving = False if len(UR5.getAllTargets()) == 0 else True
    
    if currentMove == 1:
        UR5.home()
        window.controlMenu.testMenu.buttonBack.setEnabled(False)
        currentMove = 0
        return   
        
    if currentMove > 0 and not moving:
        currentMove -= 1
        UR5.moveTCP(moves[currentMove-1]["move"], moves[currentMove]["type"])

def nextMove():
    global currentMove
    moving = False if len(UR5.getAllTargets()) == 0 else True
    
    if currentMove < len(moves) and not moving:
        UR5.moveTCP(moves[currentMove]["move"], moves[currentMove]["type"])
        currentMove += 1
    
    if currentMove == len(moves):
        window.controlMenu.testMenu.buttonNext.setEnabled(False)
    

def updateUI():
    colors = objRec.get_colors()
    window.cellDisplay.update_colors(colors)
    

def resetAuto():
    global currentMove
    currentMove = 0
    global moves
    
    moves = []
    
    UR5.resetProgram()
    
    while UR5.getStatus() == "running":
        pass
    
    UR5.home()
    
    updateUI()
    
    generateCellFrames()
    generateMoves()


def resetDebug():
    global currentMove
    global moves
    
    moves = []
    currentMove = 0
    UR5.home()
    
    updateUI()
    
    generateCellFrames()
    generateMoves()
    
window = MainWindow()

def main():
    generateCellFrames()
    generateMoves()
    window.controlMenu.autoMenu.setFunctionStart(runAutoRobot) # Set the function to be called when the button is pressed
    window.controlMenu.testMenu.setFunctionNext(nextMove) # Set the function to be called when the button is pressed
    window.controlMenu.autoMenu.setFunctionStop(stopAutoRobot) # Set the function to be called when the button is pressed
    window.controlMenu.testMenu.setFunctionBack(priorMove) # Set the function to be called when the button is pressed
    window.controlMenu.autoMenu.setFunctionReset(resetAuto)
    window.controlMenu.testMenu.setFunctionReset(resetDebug)
    
    updateUI()
    
    window.runUI() # Run the GUI
    
#stuff so you can ctrl+c to exit the program
try:
    main()
    
except KeyboardInterrupt:
    print("Disconnected from robot")
    UR5.kill()
    sys.exit()





