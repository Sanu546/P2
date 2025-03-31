import sys
from rtde_stuff.rtde_com import RTDEConnection
import time
import numpy as np
from gui.P2_GUI import MainWindow
import vision.objRec as objRec
from pose import Pose
from typing import List
import threading as th
from numpy.linalg import inv

UR5 = RTDEConnection() # Connnect to the UR5 robot

moves = [] # The moves that the robot will make

cellSpacingX = 0.1 # The spacing between the cells in the x direction
cellSpacingY = 0.1 # The spacing between the cells in the y direction

currentMove = 0

clearHeight = -0.05


ur5Frame = Pose("UR5", np.array([[1,     0,     0,   0],
                                [0,     1,     0,   0],
                                [0,     0,     1,   0],
                                [0,     0,     0,   1]])) # The frame for the UR5 robot


currentCalibrationFrame = ur5Frame # The current calibration frame

# The frame for the ramp
rampFrame = Pose("Ramp", np.array([[    -0.999673,    -0.024494,     0.007347,   .201236369], 
    [-0.023483,     0.765548,    -0.642950,  -.657846558],
    [0.010124,    -0.642913,    -0.765873,   .283486816],
    [0.000000,     0.000000,     0.000000,     1.000000 ]]
))

cellFrames: List[Pose] = [] # The frames for the cells

dropOffFrame = Pose("Dropoff", np.array([[1, 0, 0, 0.5],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]]), rampFrame) # The frame for the drop off location

baseFrames: List[Pose] = [
    ur5Frame,
    rampFrame,
    ]

def generateCellFrames():
    for i in range(4):  
        for j in range(2):
            cellFrames.append(Pose(f"Cell [{i}, {j}]", np.array([[    1,     0,     0,   j*cellSpacingX ],
            [0,     1,     0,   i*cellSpacingY ],
            [0,     0,     1,   0 ],
            [0,     0,     0,     1 ]]), rampFrame, isCell = True, color = "blue"))

def generateMoves():
    for cell in cellFrames:
        if cell.isEmpty:
            continue
        moves.append({"name": f"{cell.name} ingoing approach", "move": cell.getApproach(), "type": "j"})
        moves.append({"name": f"{cell.name}","move": cell.getGlobalPos(), "type": "l"})
        moves.append({"name": f"{cell.name} outgoing approach","move": cell.getApproach(), "type": "l"})
        moves.append({"name": f"{dropOffFrame.name} ingoing approach","move": dropOffFrame.getApproach(), "type": "j"})
        moves.append({"name": f"{dropOffFrame.name}","move": dropOffFrame.getGlobalPos(), "type": "l"})
        moves.append({"name": f"{dropOffFrame.name} outgoing approach","move": dropOffFrame.getApproach(), "type": "l"})

def runAutoRobot():
    status = UR5.getStatus()
    movesLeft = len(UR5.getAllTargets())
    window.controlMenu.buttonTest.setEnabled(False)
    window.controlMenu.buttonWork.setEnabled(False)
    

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
    window.dropdownStacker.cellDisplay.update_colors(colors)
    

def resetAuto():
    global currentMove
    global moves
    
    moves = []
    currentMove = 0
    
    if window.controlMenu.getCurrentMode() == "auto":
        UR5.resetProgram()
        while len(UR5.getAllTargets()) != 0:
            pass
    
    currentPosition = UR5.getCurrentPos() 
    posInBaseFrame = posInBase(currentPosition, rampFrame) # The position of the robot in the base frame
    zValue = posInBaseFrame[2][3]# The z axis of the base frame
    
    if zValue > clearHeight:
        print(posInBaseFrame,"Before adjustment")
        posInBaseFrame[2][3] = clearHeight # Set the z axis to the clear height
        print(posInBaseFrame,"After adjustment")
        
    UR5.moveTCPandWait(getGlobalPos(posInBaseFrame, rampFrame), "l") # Move the robot to the clear height
    UR5.home()
    updateUI()
    generateMoves()
    window.controlMenu.buttonTest.setEnabled(True)
    window.controlMenu.buttonWork.setEnabled(True)

def posInBase(frame: np.array, pose: Pose):
    base = pose.matrix
    return  inv(base) @ frame # The position of the frame in the base frame

def getGlobalPos(frame: np.array, pose: Pose):
    return pose.getGlobalPos() @ frame # The position of the frame in the global frame

def resetDebug():
    global currentMove
    global moves
    currentMove = 0
    moves = []
    
    UR5.home()
    updateUI()
    generateMoves()

def baseFrameChanged(index):
    currentCalibrationFrame = baseFrames[index]
    print("Base frame changed to:", currentCalibrationFrame.name)

def u

def updateProgramProgress():
    while True:
        currentMode = window.controlMenu.getCurrentMode() 
        if currentMode == "auto":
            if len(UR5.getAllTargets()) == 0 or len(moves) == 0:
                window.controlMenu.setProgress(0,0)
                window.controlMenu.setCurrentTarget("None")
                window.controlMenu.setNextTarget("None")
                continue
            currentAutoMove = len(moves) - len(UR5.getAllTargets())  
            window.controlMenu.setProgress(currentAutoMove + 1, len(moves))
            window.controlMenu.setCurrentTarget(moves[currentAutoMove]["name"])
            window.controlMenu.setNextTarget(moves[currentAutoMove+1]["name"])
        else:
            if(currentMove == 0):
                window.controlMenu.setProgress(0,len(moves))
                window.controlMenu.setCurrentTarget("None")
                window.controlMenu.setNextTarget("None")
                continue
            window.controlMenu.setProgress(currentMove, len(moves))
            window.controlMenu.setCurrentTarget(moves[currentMove-1]["name"])
            window.controlMenu.setNextTarget(moves[currentAutoMove]["name"])
        
        time.sleep(0.1)

    
window = MainWindow()
progressThread = th.Thread(target=updateProgramProgress)
progressThread.daemon = True

def main():
    
    generateCellFrames()
    generateMoves()
    progressThread.start()
    window.controlMenu.autoMenu.setFunctionStart(runAutoRobot) # Set the function to be called when the button is pressed
    window.controlMenu.testMenu.setFunctionNext(nextMove) # Set the function to be called when the button is pressed
    window.controlMenu.autoMenu.setFunctionStop(stopAutoRobot) # Set the function to be called when the button is pressed
    window.controlMenu.testMenu.setFunctionBack(priorMove) # Set the function to be called when the button is pressed
    window.controlMenu.autoMenu.setFunctionReset(resetAuto)
    window.controlMenu.testMenu.setFunctionReset(resetAuto)
    window.dropdownStacker.calibrator.dropdown.addItems(map(lambda base: base.name, baseFrames)) # Add the base frames to the dropdown menu
    window.dropdownStacker.calibrator.setFunctionChangeBase(baseFrameChanged) # Connect the dropdown menu to the function
    
    updateUI()
    
    window.runUI() # Run the GUI
    
main()






