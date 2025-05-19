import sys
from rtde_stuff.rtde_com import RTDEConnection # Connect to the UR5 robot
import time
import numpy as np
from gui.P2_GUI import MainWindow
import vision.objRec as objRec
from util.pose import Pose
from typing import List
from end_effector.end_effector_control import GripperController
import threading as th
from numpy.linalg import inv
import util.matrixConversion as mc
import pickle # nyt sanu
from threads.executeThread import ExcecuteThread# Import the execute thread class
from threads.execureSeriesThread import ExcecuteSeriesThread # Import the execute series thread class
#from PyQt6.QtCore import Qt, QTimer

UR5 = RTDEConnection() # Connect to the UR5 robot
gripper = GripperController(UR5) # Associate the gripper with the UR5 Controller # Create a thread to execute the actions

actions = [] # The moves that the robot will make

cellSpacingX = 0.0695 # The spacing between the cells in the x direction in meters
cellSpacingY = 0.047 # The spacing between the cells in the y direction in meters

currentAction = 0

cellsAdded = False

clearHeight = -0.05

colors = [['red', 'blue'], ['red', 'red'], ['blue', 'grey'], ['red','blue']]

# List for every frame
Frames: List[Pose] = [] # The frames for the robot

# Store the last frame before calibration
lastFrame = None
calibrationReset = False #Bool to check if the calibration is resetting
calibrationActive = False

resetEvent = th.Event() # Create a reset event
autoThread = None # Create a thread to execute the actions

# Give the seachlist a name and id if need to get the specific object you want to use    
def seachlist(name = "",id = None, matrix = []):
    number = []
    ideList:List[Pose] = []
    
    
    if id != None: # check if there are id
        ideList = list(filter(lambda x: x.id == id, Frames)) # The funtion filter list for id. The put in the list. If didn't use list it would be object with diffent items
    elif matrix != []: # check if there are matrix
        ideList = list(filter(lambda x: np.array_equal(x.getGlobalPos(), matrix), Frames)) # The funtion filter list for matrix. The put in the list. If didn't use list it would be object with diffent items
    else:
        ideList = list(filter(lambda x: x.name == name, Frames))# The funtion filter list for name. The put in the list. If didn't use list it would be object with diffent items
    
    if len(ideList) > 1 : #check if there more object with the same name 
        print("There are more object with same propty in the list")
        print(f"There are {len(ideList)} object with same name give more id !!!!!!!!")
        for i in range(len(ideList)): # show diffent object with same name
            print(f"Object {i}: {ideList[i].name} with id: {ideList[i].id} and description: {ideList[i].description}")
            print("============================================================================")
            print("                                                                            ")
        return
    elif(len(ideList) == 0):
        print("There are no object with the property in the list")
        return
    
    return ideList[0] # return the first object in the list

def deleteFrame(index):
    Frames.pop(index)
    
def replaceFrames(oldFrame,newFrame):
    global Frames
    Frames[Frames.index(oldFrame)] = newFrame 
    for index, baseFrame in enumerate(baseFrames):
        if baseFrame.id == oldFrame.id:
            baseFrames[index] = newFrame # Replace the base frame in the list of frames
            for frameIndex, frame in enumerate(Frames):
                if frame.base == None:
                    continue
                if frame.base.id == oldFrame.id:
                    Frames[frameIndex].base = newFrame
    
    #saveList() # Save the the new frame to the list  

cellFrames: List[Pose] = [] # The frames for the cells
 # The frame for the drop off location
# The frames for the robot and the ramp

ur5Frame = Pose(1 ,"UR5", np.array([[1,     0,     0,   0],
                                [0,     1,     0,   0],
                                [0,     0,     1,   0],
                                [0,     0,     0,   1]]),"UR5 frame for the robot for simulation Final_BetaBackup Date: 09-04-2025", base=None) # The frame for the UR5 robot
rampFrame = Pose(2, "Ramp", np.array([[    -1.000000,     0.000001,     0.000005,   .172217000 ],
     [-0.000001,     0.906308,    -0.422618,  -.302361000 ],
     [-0.000005,    -0.422618,    -0.906308,    .044797000 ],
      [0.000000,     0.000000,     0.000000,     1.000000 ]]),"Ramp frame for the robot for simulation Final_BetaBackup Date: 09-04-2025", base = None)
Frames.append(ur5Frame) # Add the UR5 frame to the list of frames
Frames.append(rampFrame) # Add the ramp frame to the list of frames

dropOffFrame = Pose(3, "Dropoff", np.array([[1, 0, 0, 0.029823],
                              [0, 1, 0, -.284189],
                              [0, 0, 1, .010],
                              [0, 0, 0, 1]]), "Dropoff frame for the used cell", base = seachlist("Ramp")) # The frame for the drop off location
evbFrame = Pose(4, "EVB", np.array([[1, 0, 0, 0.151265],
                                [0, 1, 0, -.044],
                                [0, 0, 1, .006],
                                [0, 0, 0, 1]]),"EVB frame for the robot for simulation Final_BetaBackup Date: 09-04-2025", base = seachlist("Ramp")) # The frame for the EVB location
Frames.append(dropOffFrame) # Add the drop off frame to the list of frames
Frames.append(evbFrame) # Add the EVB frame to the list of frames

pickUpFrame = Pose(5, "Pickup", np.array([[     1.000000,    -0.00000,    -0.000000,    .085406 ],
      [0.00000,     1.000000,    -0.00000,  -.02500 ],
      [0.000000,     0.00000,     1.000000,     .010 ],
      [0.000000,     0.000000,     0.000000,     1.000000 ]
]),"Lid pickup frame for the robot for simulation Final_BetaBackup Date: 09-04-2025", base = seachlist("Ramp")) # The frame for the lid pickup location
Frames.append(pickUpFrame) # Add the lid pickup frame to the list of frames  
     
lidOnEvbFrame = Pose(6, "LidOnEvb", np.array([[    -0.000000,    -1.000000,     0.000000,   .1865000 ],
      [1.000000,     0.000000,     0.000000,  -.1152000 ],
      [0.000000,     0.000000,     1.000000,   -.05464000 ],
      [0.000000,     0.000000,     0.000000,     1.000000 ]]), "Lid frame when the lid is on the EVB", base = seachlist("Ramp"), approach=0.15) # The frame for the lid location
Frames.append(lidOnEvbFrame) # Add the lid frame to the list of frames

lidStorageFrame = Pose(7, "LidStorage", np.array([[     0.000001,    -0.000001,     1.000000,   -.097682807 ],
     [0.000000,    1.000001,     0.000001,  -.590749490 ],
      [-1.000001,    0.000000,    -0.000001,   .111500174 ],
      [0.000000,     0.000000,     0.000000,     1.000000 ]]), "Lid frame when the lid is in the storage") # The frame for the lid location
Frames.append(lidStorageFrame) # Add the lid frame to the list of frames

lidStorageAproachFrame = Pose(8, "LidStorageAproach", np.array([[     1,    0,    0,   -.145143],
    [0,     1,    0,    0],
    [0,     0,    1,    0 ],
    [0,     0,     0,     1 ]]), "Lid frame when the lid is in the storage", base = seachlist("LidStorage")) # The frame for the lid location
Frames.append(lidStorageAproachFrame) # Add the lid frame to the list of frames

lidStorageViaFrame = Pose(9, "LidStorageVia", np.array([[     1,    0,    0,   -.2],
    [0,     1,    0,  0],
    [0,     0,    1,    0 ],
    [0,     0,     0,     1 ]]), "Lid frame when the lid is in the storage", base = seachlist("LidStorage")) # The frame for the lid location
Frames.append(lidStorageViaFrame) # Add the lid frame to the list of frames


lidStorageReturnPos = np.array([np.radians(61.295092), np.radians(-99.176599), np.radians(109.691574), np.radians(56.953220), np.radians(77.815347), np.radians(-205.378034)])

def saveList():    
    with open('saves/Frames.pkl', "wb") as file:
        pickle.dump(Frames, file)  # Save Pose to a file 
        print("Frames saved successfully")

def loadList():
    with open('saves/Frames.pkl', "rb") as file:
        return pickle.load(file)  # Load Pose from the file

# Er den ikke forkte da det skal være realtive første bokse.
def generateCellFrames(): 
    rampFrame = seachlist("Ramp") # The frame for the ramp
    evbFrame = seachlist("EVB") # The frame for the EVB location

    evbX = evbFrame.matrix[0][3] # The x position of the EVB frame
    evbY = evbFrame.matrix[1][3] # The y position of the EVB frame
    evbZ = evbFrame.matrix[2][3] # The z position of the EVB frame
    
    for i in range(4):  
        for j in range(2):
            newFrame = Pose((int(f"{i}{j}{00}")),f"Cell [{i}, {j}]", np.array([[    1,     0,     0,   j*cellSpacingX+evbX ],
            [0,     1,     0,   -i*cellSpacingY+evbY ],
            [0,     0,     1,   evbZ ],
            [0,     0,     0,     1 ]]),"Cell n frame for the robot Date: 09-04-2025" , rampFrame, isCell = True, color = colors[i][j-1])
            oldFrame = seachlist(f"Cell [{i}, {j}]") # The old frame in the list of frames
            if oldFrame == None: # Check if the frame is already in the list
                Frames.append(newFrame)
            else:
                replaceFrames(oldFrame, newFrame) # Replace the old frame with the new frame   
#Calibration variables
# tidligere: ur5Frame # The current calibration frame

            
# is show every object in the list of frames. Where can se name,id,matrix and description
def showFramesInList():
    print(f"There are {len(Frames)} frames in the list")
    print("============================================================================") 
    for i in range(len(Frames)):
        print(f"Frame {i}: {Frames[i].name}")
        print(f"Is cell: {Frames[i].id}")
        print("Matrix: ")
        print(Frames[i].matrix)
        print(f"Description: {Frames[i].description}")
        print("============================================================================")
        print("                                                                            ")
 
def generateMoves():
    lidOnEvbFrame = seachlist("LidOnEvb") # The frame for the lid on the EVB location
    lidStorageFrame = seachlist("LidStorage") # The frame for the lid in the storage location
    lidStorageAproachFrame = seachlist("LidStorageAproach") # The frame for the lid in the storage location
    lidStorageViaFrame = seachlist("LidStorageVia")
    
    actions.append({"frameID":lidOnEvbFrame.id, "actionType": "moveTCP", "name": "Lid on EVB ingoing approach", "move": lidOnEvbFrame.getApproach(), "type": "j"})
    actions.append({"actionType": "gripper", "name": "Gripper open", "mode": "position", "position": "lidopen"}) # Open the gripper
    actions.append({"frameID":lidOnEvbFrame.id, "actionType": "moveTCP", "name": "Lid on EVB", "move": lidOnEvbFrame.getGlobalPos(), "type": "l"}) # Move to the lid on the EVB location
    actions.append({"actionType": "gripper", "name": "Gripper close", "mode": "position", "position": "lidclose"}) # Close the gripper
    actions.append({"frameID":lidOnEvbFrame.id, "actionType": "moveTCP", "name": "Lid on EVB outgoing approach", "move": lidOnEvbFrame.getApproach(), "type": "l"}) # Move to the lid on the EVB location
    actions.append({"frameID":lidStorageAproachFrame.id , "actionType": "moveTCP", "name": "Lid storage ingoing approach", "move": lidStorageAproachFrame.getGlobalPos(), "type": "j"}) # Move to the lid storage location
    #actions.append({"actionType": "vision", "name": "Vision capture"}) # Capture a vision frame to evaluate    
    actions.append({"frameID":lidStorageFrame.id , "actionType": "moveTCP", "name": "Lid storage", "move": lidStorageFrame.getGlobalPos(), "type": "l"}) # Move to the lid storage location
    actions.append({"actionType": "gripper", "name": "Gripper open", "mode": "position", "position": "lidopen"}) # Open the gripper
    actions.append({"frameID":lidStorageFrame.id , "actionType": "moveTCP", "name": "Lid storage outgoing approach", "move": lidStorageFrame.getApproach(), "type": "l"}) # Move to the lid storage location
    actions.append({"frameID":lidStorageViaFrame.id, "actionType": "moveTCP", "name": "Lid Storage outgoing via approach", "move":lidStorageViaFrame.getApproach(), "type": "j"})
    actions.append({"actionType": "setJoints", "name": "Lid Storage outgoing pos", "move": lidStorageReturnPos})
            
    #print(actions)

def generateCellMoves():
    for i in range(4):
        for j in range(2):
            cell = seachlist(f"Cell [{i}, {j}]")
            dropOffFrame = seachlist("Dropoff")
            pickUpFrame = seachlist("Pickup")
            if cell.replace: # Check if the cell is a replace cell
                actions.append({"frameID":cell.id, "actionType": "moveTCP", "name": f"{cell.name} ingoing approach", "move": cell.getApproach(), "type": "j"})
                actions.append({"actionType": "gripper", "name": "Gripper open", "mode": "position", "position": "blockopen"})
                actions.append({"frameID":cell.id, "actionType": "moveTCP", "name": f"{cell.name}","move": cell.getGlobalPos(), "type": "l"})
                actions.append({"actionType": "gripper", "name": "Gripper close", "mode": "position", "position": "blockclose"})
                actions.append({"frameID":cell.id, "actionType": "moveTCP", "name": f"{cell.name} outgoing approach","move": cell.getApproach(), "type": "l"})
                actions.append({"frameID":dropOffFrame.id, "actionType": "moveTCP", "name": f"{dropOffFrame.name} ingoing approach","move": dropOffFrame.getApproach(), "type": "j"})
                actions.append({"frameID":dropOffFrame.id, "actionType": "moveTCP", "name": f"{dropOffFrame.name}","move": dropOffFrame.getGlobalPos(), "type": "l"})
                actions.append({"actionType": "gripper", "name": "Gripper open", "mode": "position", "position": "blockopen"})
                actions.append({"frameID":dropOffFrame.id, "actionType": "moveTCP", "name": f"{dropOffFrame.name} outgoing approach","move": dropOffFrame.getApproach(), "type": "l"})
                
            if cell.isEmpty or cell.replace: # Check if the cell is empty and not a replace cell
                actions.append({"frameID":pickUpFrame.id, "actionType": "moveTCP", "name": f"{pickUpFrame.name} ingoing approach","move": pickUpFrame.getApproach(), "type": "j"})
                actions.append({"frameID":pickUpFrame.id, "actionType": "moveTCP", "name": f"{pickUpFrame.name}","move": pickUpFrame.getGlobalPos(), "type": "l"})  
                actions.append({"actionType": "gripper", "name": "Gripper close", "mode": "position", "position": "blockclose"})
                actions.append({"frameID":pickUpFrame.id, "actionType": "moveTCP", "name": f"{pickUpFrame.name} outgoing approach","move": pickUpFrame.getApproach(), "type": "l"})
                actions.append({"frameID":cell.id, "actionType": "moveTCP", "name": f"{cell.name} ingoing approach","move": cell.getApproach(), "type": "j"})
                actions.append({"frameID":cell.id, "actionType": "moveTCP", "name": f"{cell.name}","move": cell.getGlobalPos(), "type": "l"})
                actions.append({"actionType": "gripper", "name": "Gripper open", "mode": "position", "position": "blockopen"})
                actions.append({"frameID":cell.id, "actionType": "moveTCP", "name": f"{cell.name} outgoing approach","move": cell.getApproach(), "type": "l"})
    
def singleAction(action):
    exeThread = ExcecuteThread(action, UR5, gripper, window, updateUI) # Create a thread to execute the action
    exeThread.start()
    
def runAutoRobot():
    global autoThread
    
    status = UR5.getStatus()
    actionsLeft = len(UR5.getAllTargets())
    window.controlMenu.buttonTest.setEnabled(False)
    window.controlMenu.buttonWork.setEnabled(False)

    if actionsLeft != 0 and status == "running":
        print("Robot is already running")
        return
    
    if actionsLeft !=0 and status == "idle":
        UR5.resume()
        return
    autoThread = ExcecuteSeriesThread(actions, UR5, gripper, resetEvent, updateUI) # Create a thread to execute the actions
    autoThread.start() # Start the thread

def stopAutoRobot():
    UR5.stop()  

def getCurrentFrame(action):
    if action["actionType"] == "moveTCP":
        print("Current id: ", action["frameID"])
        currentFrame = seachlist(id=int(action["frameID"]))
        print("Setting current frame: ", currentFrame.name)
        isApproach = False
        
        if(not np.array_equal(currentFrame.getGlobalPos(), action["move"])):
            isApproach = True
            
        return currentFrame, isApproach
    
    return None, False
    

def priorMove():
    global currentAction
    moving = False if len(UR5.getAllTargets()) == 0 else True
    
    if currentAction == 1:
        UR5.home()
        window.controlMenu.testMenu.buttonBack.setEnabled(False)
        window.controlMenu.buttonTest.setEnabled(True)
        window.controlMenu.buttonWork.setEnabled(True)
        currentAction = 0
        window.dropdownStacker.calibrator.setCurrentFrame(None, False) # Set the current frame in the UI
        return   
        
    if currentAction > 0 and not moving:
        currentAction -= 1
        singleAction(actions[currentAction-1])
        
        currentFrame, isApporach = getCurrentFrame(actions[currentAction-1])
        if currentFrame != None:
            window.dropdownStacker.calibrator.setCurrentFrame(currentFrame, isApporach)
    

def nextMove():
    global currentAction
    moving = False if len(UR5.getAllTargets()) == 0 else True
    
    currentFrame, isApporach = getCurrentFrame(actions[currentAction])
    if currentFrame != None:
        window.dropdownStacker.calibrator.setCurrentFrame(currentFrame, isApporach) # Set the current frame in the UI
    
    if currentAction < len(actions) and not moving:
        singleAction(actions[currentAction])
        # executeAction(actions[currentAction-1])
        currentAction += 1
    
    if currentAction == len(actions):
        window.controlMenu.testMenu.buttonNext.setEnabled(False)
    
    window.controlMenu.buttonTest.setEnabled(False)
    window.controlMenu.buttonWork.setEnabled(False)

def updateUI():
    global colors
    #colors = objRec.get_colors()
    print("Colors: ", colors)
    window.dropdownStacker.cellDisplay.update_colors(colors)
    
def reset():
    global currentAction
    global actions
    global autoThread
    global cellsAdded
    rampFrame = seachlist("Ramp") # The frame for the ramp sanu 
    actions = []
    currentAction = 0
    
    if window.controlMenu.getCurrentMode() == "auto":
        resetEvent.set() # Set the reset event to stop the auto thread
        print("Waiting for auto thread to finish...")
        
        if(UR5.isStopped()):
            UR5.resetRobot()
        
        autoThread.join()
        print("Auto thread finished.")
        while len(UR5.getAllTargets()) != 0:
            pass
        
    currentPosition = UR5.getCurrentPos() 
    posInBaseFrame = posInBase(currentPosition, rampFrame) # The position of the robot in the base frame 
    zValue = posInBaseFrame[2][3]# The z axis of the base frame
    
    if zValue > clearHeight:
        posInBaseFrame[2][3] = clearHeight # Set the z axis to the clear height
        
    homeActions = []
    homeActions.append({"actionType": "moveTCP", "name": "ClearHeight", "move": getGlobalPos(posInBaseFrame, rampFrame), "type": "j"})
    homeActions.append({"actionType": "home", "name": "Homing"})
    
    homingThread = ExcecuteSeriesThread(homeActions, UR5, gripper) # Create a thread to execute the actions
    homingThread.start() # Start the thread
    homingThread.join()
    
    updateUI()
    actions = []
    generateMoves()
    
    window.controlMenu.buttonTest.setEnabled(True)
    window.controlMenu.buttonWork.setEnabled(True)
    
    cellsAdded = False
    
    

def onChangeToAutoMode():
    window.dropdownStacker.calibrator.startCal.setEnabled(False) # Disable the calibrator button
    
def onChangeToCalMode():
    window.dropdownStacker.calibrator.startCal.setEnabled(True) # Enable the calibrator button

def posInBase(frame: np.array, pose: Pose):
    base = pose.matrix
    return  inv(base) @ frame # The position of the frame in the base frame

def getGlobalPos(frame: np.array, pose: Pose):
    if(pose == None):
        return frame # If the pose is None, return the frame
    
    return pose.getGlobalPos() @ frame # The position of the frame in the global frame

def baseFrameChanged(index):
    global currentCalibrationFrame
    currentCalibrationFrame = baseFrames[index]
    updateUIPosition()
    print("Base frame changed to:", currentCalibrationFrame.name)
    
def calibrateRobot():
    global calibrationActive
    global lastFrame
    
    lastFrame = UR5.getCurrentPos() # The last frame before calibration
    window.controlMenu.testMenu.buttonNext.setEnabled(False)
    window.controlMenu.testMenu.buttonBack.setEnabled(False)
    window.controlMenu.testMenu.buttonReset.setEnabled(False)
    calibrationActive = True

# the frame you want in the list remeber to change every thing 
# replace = Pose(len(Frames)+1,"Dropoff", np.array([[1, 0, 0, 0.5],
#                               [0, 1, 0, 0],
#                               [0, 0, 1, 0],
#                               [0, 0, 0, 1]]),"Dropoff first frame for the robot Date: 04-04-2025",Frames[1])
  

# skal listen moves
def stopCalibration():
    global calibrationActive
    window.controlMenu.testMenu.buttonNext.setEnabled(True)
    window.controlMenu.testMenu.buttonBack.setEnabled(True)
    window.controlMenu.testMenu.buttonReset.setEnabled(True)
    calibrationActive = False

def resetCalibration():
    global lastFrame
    
    print("Last Frame:", lastFrame)
    if lastFrame[0][0] == None or not calibrationActive:
        print("Reset calibration: No last frame or not in calibration mode")
        print("Laste frame:", lastFrame)
        print("Calibration active:", calibrationActive)
        return
    
    lastFrame = Pose(999, "temp", lastFrame) # The last frame before calibration
    resetAction = {"actionType": "moveTCP", "name": "Reset calibration", "move": lastFrame.getGlobalPos(), "type": "l"}
    
    
    singleAction(resetAction) # Move the robot to the last frame
    stopCalibration() # Stop the calibration
    lastFrame = None # Reset the last frame

def saveSingeCalibrationFrame():
    global actions
    print("Saving single calibration frame")
    
    newMatrix = window.dropdownStacker.calibrator.getCalPosition()

    oldFrame: Pose = window.dropdownStacker.calibrator.currentFrame
    isApproach = window.dropdownStacker.calibrator.currentFrameIsApproach # Check if the current frame is an approach frame
    
    newFrame: Pose = oldFrame
    
    if newFrame.base != currentCalibrationFrame and newFrame.base != None:
        globalPos = getGlobalPos(newMatrix, currentCalibrationFrame) # The global position of the new matrix in the base frame
        newMatrix = posInBase(globalPos, newFrame.base) # The new matrix is the old matrix multiplied by the base matrix
    
    if isApproach:
        print("This is an approach frame")
        newMatrix = newMatrix @ inv(oldFrame.approach) # The new matrix is the old matrix multiplied by the approach matrix
    
    newFrame.matrix = newMatrix # Update the calibration frame with the new matrix
    replaceFrames(oldFrame, newFrame) # Replace the calibration frame with the new matrix
    
    actions = []
    generateMoves()
    generateCellMoves()
    stopCalibration()
    window.dropdownStacker.calibrator.stopCalibration()
    saveList()
    print("Calibration frame saved, and cal stopped")
    
def saveBaseCalibrationFrame():
    global actions
    
    newMatrix = window.dropdownStacker.calibrator.getCalPosition()
    oldFrame: Pose = window.dropdownStacker.calibrator.currentFrame # The current frame in the UI
    newBase: Pose = oldFrame.base # The base frame of the current frame
    
    if currentCalibrationFrame.name != "UR5":
        newMatrix = getGlobalPos(newMatrix, currentCalibrationFrame) # The global position of the new matrix in the base frame
    
    localPos = oldFrame.matrix
    newBaseMatrix = newMatrix @ inv(localPos)
    
    newBase.matrix = newBaseMatrix # The new matrix is the old matrix multiplied by the base matrix
    
    replaceFrames(oldFrame.base, newBase) # Replace the base frame with the new matrix
    
    actions = []
    generateMoves()
    generateCellMoves()
    stopCalibration()
    window.dropdownStacker.calibrator.stopCalibration()
    saveList()
    
def saveApproachCalibrationFrame():
    print("Saving approach calibration frame")
    global actions
    
    newMatrix = window.dropdownStacker.calibrator.getCalPosition()
    oldFrame: Pose = window.dropdownStacker.calibrator.currentFrame # The current frame in the UI
    
    if(currentCalibrationFrame.name != "UR5"):
        newMatrix = getGlobalPos(newMatrix, currentCalibrationFrame)
    
    newMatrix = inv(oldFrame.getGlobalPos()) @ newMatrix  # The new matrix is the old matrix multiplied by the base matrix
    
    newFrame: Pose = oldFrame # The new frame is the old frame
    newFrame.approach = newMatrix # The new approach matrix is the new matrix
    
    replaceFrames(oldFrame, newFrame) # Replace the calibration frame with the new matrix
    
    actions = []
    generateMoves()
    generateCellMoves()
    stopCalibration()
    window.dropdownStacker.calibrator.stopCalibration()
    saveList()


def translateFrame(axis, value):
    try:
        value = float(value)
    except ValueError:
        print("Invalid value:", value)
        return
    #print("Translating along:", axis, "by:", value)
    tempFrame = Pose(999, "temp", posInBase(UR5.getCurrentPos(), currentCalibrationFrame), base = currentCalibrationFrame) # The current position of the robot
    
    window.dropdownStacker.calibrator.enableInput(False)
    
    if axis == "x":
        tempFrame.matrix[0][3] = value * 0.001
    elif axis == "y":
        tempFrame.matrix[1][3] = value * 0.001
    elif axis == "z":
        tempFrame.matrix[2][3] = value * 0.001
    
    UR5.moveTCPandWait(tempFrame.getGlobalPos(), "l") # Move the robot to the new position
    #print("Moved to:", UR5.getCurrentPos())
    window.dropdownStacker.calibrator.enableInput(True)

def rotateFrame(values): 
    try:
        values[0] = np.radians(float(values[0]))
        values[1] = np.radians(float(values[1]))
        values[2] = np.radians(float(values[2]))
    except ValueError:
        print("Invalid values:", values)
        return
    
    window.dropdownStacker.calibrator.enableInput(False)
    
    tempFrame = Pose(999, "temp", posInBase(UR5.getCurrentPos(), currentCalibrationFrame), base = currentCalibrationFrame) # The current position of the robot
    newR = mc.RPYtoRMatrix(values) # The new rotation matrix
    tempFrame.matrix[:3, :3] = newR # Set the rotation matrix in Frame matirx to the new rotation matrix
    R = tempFrame.matrix[:3, :3]
    
    
    UR5.moveTCPandWait(tempFrame.getGlobalPos(), "l") # Move the robot to the new position
    
    window.dropdownStacker.calibrator.enableInput(True)  
    
def updateUIPosition():
    currentPosition = posInBase(UR5.getCurrentPos(), currentCalibrationFrame) # The current position of the robot in the base frame
    currentRPY =  mc.matrixToRPY(currentPosition)
    # print("Current position in base frame:", currentPosition)
    # print("Current position:", currentRPY)
    window.dropdownStacker.calibrator.setCurrentPose(currentRPY) # Update the current pose in the UI
    
def updateProgramProgress():
    while True:
        global cellsAdded
        global calibrationReset
        if not calibrationActive:
            updateUIPosition() # Update the current pose in the UI
            
        currentMode = window.controlMenu.getCurrentMode() 
        if currentMode == "auto":
            if autoThread == None or not autoThread.is_alive():
                window.controlMenu.setProgress(0,0)
                window.controlMenu.setCurrentTarget("None")
                window.controlMenu.setNextTarget("None")
                continue
            
            currentTarget, nextTarget, currentProgress = autoThread.getState()
            
            if currentTarget == "Lid storage":
                updateUI()
            if currentTarget == "Lid storage outgoing approach":
                if not cellsAdded:
                    generateCellFrames()
                    generateCellMoves()
                    #autoThread.addToSeries(actions[9:])
                    cellsAdded = True
                
                
            if currentTarget == None or currentProgress == None:
                window.controlMenu.setProgress(0,0)
                window.controlMenu.setCurrentTarget("None")
                window.controlMenu.setNextTarget("None")
                continue
            
            window.controlMenu.setProgress(currentProgress + 1, len(actions))
            window.controlMenu.setCurrentTarget(currentTarget)
            if(nextTarget == None):
                window.controlMenu.setNextTarget("None")
            
            window.controlMenu.setNextTarget(nextTarget)
        else:
            if(currentAction == 0):
                window.controlMenu.setProgress(0,len(actions))
                window.controlMenu.setCurrentTarget("None")
                window.controlMenu.setNextTarget("None")
                continue
            currentProgress = currentAction
            window.controlMenu.setProgress(currentProgress, len(actions))
            
            currentTarget = actions[currentAction-1]["name"]
            
            if currentTarget == "Lid storage":
                updateUI()
            if currentTarget == "Lid storage outgoing approach":
                if not cellsAdded:
                    generateCellFrames()
                    generateCellMoves()
                    cellsAdded = True
                
            nextTarget = actions[currentAction]["name"]
            window.controlMenu.setCurrentTarget(currentTarget)
            window.controlMenu.setNextTarget(nextTarget)
            
        time.sleep(0.1)


def pmatrix():
    with open('calibrationFrame.pkl', "rb") as file:
        loaded_rampFrame = pickle.load(file)
        print(loaded_rampFrame.matrix)  # Print matrix from loaded rampFrame
        
        
window = MainWindow()
progressThread = th.Thread(target=updateProgramProgress)
progressThread.daemon = True

# To replace Frames list and save new  comented out code were (1) and und commented (2) and (3). Ask Santhosh if don't understand
#Frames = loadList() # Load the frames from the file (1)

baseFrames: List[Pose] = [
    seachlist("UR5"),
    seachlist("Ramp"),
    ]

currentCalibrationFrame: Pose = seachlist("UR5")

#showFramesInList()
def main():
    updateUI()
    generateCellFrames()# If you want to generate other cells on comentar this code (2)
    #saveList()# (3)
    #showFramesInList()
    generateMoves()
    print("Actions: ", actions)
    progressThread.start()
    window.controlMenu.autoMenu.setFunctionStart(runAutoRobot) # Set the function to be called when the button is pressed
    window.controlMenu.testMenu.setFunctionNext(nextMove) # Set the function to be called when the button is pressed
    window.controlMenu.autoMenu.setFunctionStop(stopAutoRobot) # Set the function to be called when the button is pressed
    window.controlMenu.testMenu.setFunctionBack(priorMove) # Set the function to be called when the button is pressed
    window.controlMenu.autoMenu.setFunctionReset(reset)
    window.controlMenu.testMenu.setFunctionReset(reset)
    window.controlMenu.setFunctionChangeToAuto(onChangeToAutoMode) # Set the function to be called when the button is pressed
    window.controlMenu.setFunctionChangeToCal(onChangeToCalMode) # Set the function to be called when the button is pressed
    
    window.dropdownStacker.calibrator.setStartCalibration(calibrateRobot) # Set the function to be called when the button is pressed
    window.dropdownStacker.calibrator.setStopCalibration(stopCalibration) # Set the function to be called when the button is pressed
    window.dropdownStacker.calibrator.setResetCalibration(resetCalibration) # Set the function to be called when the button is pressed
    window.dropdownStacker.calibrator.saveCalDialog.setFunctionBaseUpdate(saveBaseCalibrationFrame) # Set the function to be called when the button is pressed
    window.dropdownStacker.calibrator.saveCalDialog.setFunctionSingleFrameUpdate(saveSingeCalibrationFrame) # Set the function to be called when the button is pressed
    window.dropdownStacker.calibrator.saveCalDialog.setFunctionApproachUpdate(saveApproachCalibrationFrame) # Set the function to be called when the button is pressed
    
    window.dropdownStacker.calibrator.setTranslateX(translateFrame, "x") # Set the function to be called when the button is pressed
    window.dropdownStacker.calibrator.setTranslateX(translateFrame, "x") # Set the function to be called when the button is pressed
    window.dropdownStacker.calibrator.setTranslateY(translateFrame, "y") # Set the function to be called when the button is pressed
    window.dropdownStacker.calibrator.setTranslateZ(translateFrame, "z") # Set the function to be called when the button is pressed
    window.dropdownStacker.calibrator.setRotate(rotateFrame)
    
    window.dropdownStacker.calibrator.setBaseFrames(baseFrames)
    window.dropdownStacker.calibrator.setFunctionChangeBase(baseFrameChanged) # Connect the dropdown menu to the function
    
    updateUI()
    window.controlMenu.testMenu.buttonBack.setEnabled(False) # Disable the back button
    window.runUI() # Run the GUI
    
 # Show the frames in the list
main()

 





