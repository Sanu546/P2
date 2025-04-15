import sys
from rtde_stuff.rtde_com import RTDEConnection # Connect to the UR5 robot
import time
import numpy as np
from gui.P2_GUI import MainWindow
import vision.objRec as objRec
from pose import Pose
from typing import List
from end_effector_control import GripperController
import threading as th
from numpy.linalg import inv
import matrixConversion as mc
import pickle # nyt sanu
from executeThread import ExcecuteThread# Import the execute thread class
from execureSeriesThread import ExcecuteSeriesThread # Import the execute series thread class

#from PyQt6.QtCore import Qt, QTimer

UR5 = RTDEConnection() # Connect to the UR5 robot
gripper = GripperController(UR5) # Associate the gripper with the UR5 Controller # Create a thread to execute the actions

actions = [] # The moves that the robot will make

cellSpacingX = 0.07 # The spacing between the cells in the x direction in meters
cellSpacingY = 0.046 # The spacing between the cells in the y direction in meters

currentAction = 0

clearHeight = -0.05

# List for every frame
Frames: List[Pose] = [] # The frames for the robot

resetEvent = th.Event() # Create a reset event
autoThread = None # Create a thread to execute the actions

# Give the seachlist a name and id if need to get the specific object you want to use    
def seachlist(name,id = None):
    number = []
    ideList:List[Pose] = []
    
    if id != None: # check if there are id
        for i in range(len(Frames)):
            if Frames[i].name == name and Frames[i].id == id: 
                number.append(i) #save index of object in the list 
                ideList.append(Frames[i])  
                if len(ideList) > 1 : #check if more object with same name 
                    print("There somthing wrong with the id you manuel felter the list")
                    for i in range(len(ideList)): # show diffent object with same name and id
                        print(f"Object {i}: {ideList[i].name} with id: {ideList[i].id} and description: {ideList[i].description}")
                        print(f"Object in the list is: Frames[{number[i]}]")
                        print("============================================================================")
                        print("                                                                            ")
                    print("Please change the id or name to the object you want to use wih funktion") 
                return
            elif(len(ideList) == 0):
                print("There are no object with that id and name")
                return 
        
    else:
        ideList = list(filter(lambda x: x.name == name, Frames))# The funtion filter list for name. The put in the list. If didn't use list it would be object with diffent items
        if len(ideList) > 1 : #check if there more object with the same name 
            print("There are more object with same name in the list")
            print(f"There are {len(ideList)} object with same name give more id !!!!!!!!")
            for i in range(len(ideList)): # show diffent object with same name
                print(f"Object {i}: {ideList[i].name} with id: {ideList[i].id} and description: {ideList[i].description}")
                print("============================================================================")
                print("                                                                            ")
            return
        elif(len(ideList) == 0):
            print("There are no object with name")
            return
               
       
         
   
    
    return ideList[0] # return the first object in the list


def deleteFrame(index):
    Frames.pop(index)
    
def replaceFrames(oldFrame,newFrame):
    Frames[Frames.index(oldFrame)] = newFrame 
    saveList() # Save the the new frame to the list  




cellFrames: List[Pose] = [] # The frames for the cells
 # The frame for the drop off location
# The frames for the robot and the ramp

ur5Frame = Pose(1 ,"UR5", np.array([[1,     0,     0,   0],
                                [0,     1,     0,   0],
                                [0,     0,     1,   0],
                                [0,     0,     0,   1]]),"UR5 frame for the robot for simulation Final_BetaBackup Date: 09-04-2025", base=None) # The frame for the UR5 robot
rampFrame = Pose(2, "Ramp", np.array([[    -1.000000,    -0.000001,    -0.000000,   .168199992],
     [-0.000001,     0.906308,    -0.422618,  -.301577378 ],
      [0.000001,    -0.422618,    -0.906308,    0.044323861 ],
     [ 0.000000,     0.000000,     0.000000,     1.000000 ]]),"Ramp frame for the robot for simulation Final_BetaBackup Date: 09-04-2025", base = None)
Frames.append(ur5Frame) # Add the UR5 frame to the list of frames
Frames.append(rampFrame) # Add the ramp frame to the list of frames

dropOffFrame = Pose(3, "Dropoff", np.array([[1, 0, 0, 0.0285],
                              [0, 1, 0, -.27091],
                              [0, 0, 1, .009917],
                              [0, 0, 0, 1]]), "Dropoff frame for the used cell", base = seachlist("Ramp")) # The frame for the drop off location
evbFrame = Pose(4, "EVB", np.array([[1, 0, 0, 0.14545],
                                [0, 1, 0, -.044857],
                                [0, 0, 1, .009917],
                                [0, 0, 0, 1]]),"EVB frame for the robot for simulation Final_BetaBackup Date: 09-04-2025", base = seachlist("Ramp")) # The frame for the EVB location


Frames.append(dropOffFrame) # Add the drop off frame to the list of frames
Frames.append(evbFrame) # Add the EVB frame to the list of frames

        
def saveList():   
    with open('Frames.pkl', "wb") as file:
        pickle.dump(Frames, file)  # Save Pose to a file 
        print("Frames saved successfully")
       


def loadList():
    with open('Frames.pkl', "rb") as file:
        return pickle.load(file)  # Load Pose from the file


#Frames = loadList() # Load the frames from the file
baseFrames: List[Pose] = [
    ur5Frame,
    seachlist("Ramp"),
    ]
# Er den ikke forkte da det skal være realtive første bokse.
def generateCellFrames():
    rampFrame = seachlist("Ramp") # The frame for the ramp
 
    evbX = evbFrame.matrix[0][3] # The x position of the EVB frame
    evbY = evbFrame.matrix[1][3] # The y position of the EVB frame
    for i in range(4):  
        for j in range(2):
            Frames.append(Pose(len(Frames)+1,f"Cell [{i}, {j}]", np.array([[    1,     0,     0,   j*cellSpacingX+evbX ],
            [0,     1,     0,   -i*cellSpacingY+evbY ],
            [0,     0,     1,   0 ],
            [0,     0,     0,     1 ]]),"Cell n frame for the robot Date: 09-04-2025" , rampFrame, isCell = True, color = "blue"))   




#Calibration variables
currentCalibrationFrame: Pose = seachlist("UR5") # tidligere: ur5Frame # The current calibration frame
calibrationActive = False
            
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
    for i in range(4):
        for j in range(2):
            cell = seachlist(f"Cell [{i}, {j}]")
            if cell.isEmpty:
                continue
            actions.append({"actionType": "moveTCP", "name": f"{cell.name} ingoing approach", "move": cell.getApproach(), "type": "j"})
            actions.append({"actionType": "gripper", "name": "Gripper open", "mode": "position", "position": 25})
            actions.append({"actionType": "moveTCP", "name": f"{cell.name}","move": cell.getGlobalPos(), "type": "l"})
            actions.append({"actionType": "gripper", "name": "Gripper close", "mode": "force", "force": 40})
            actions.append({"actionType": "moveTCP", "name": f"{cell.name} outgoing approach","move": cell.getApproach(), "type": "l"})
            actions.append({"actionType": "moveTCP", "name": f"{dropOffFrame.name} ingoing approach","move": dropOffFrame.getApproach(), "type": "j"})
            actions.append({"actionType": "moveTCP", "name": f"{dropOffFrame.name}","move": dropOffFrame.getGlobalPos(), "type": "l"})
            actions.append({"actionType": "gripper", "name": "Gripper open", "mode": "position", "position": 30})
            actions.append({"actionType": "moveTCP", "name": f"{dropOffFrame.name} outgoing approach","move": dropOffFrame.getApproach(), "type": "l"})
    #print(actions)

def singleAction(action):
    exeThread = ExcecuteThread(action, UR5, gripper, window) # Create a thread to execute the action
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
    autoThread = ExcecuteSeriesThread(actions, UR5, gripper, resetEvent) # Create a thread to execute the actions
    autoThread.start() # Start the thread

def executeActions():
    global currentAction
    for action in actions:
        #print(f"TS: {time.time()} Action: {action}") # Debugging
        print(f"Made it here, action: {action}")
        executeAction(action) # Where the magic hapens
        currentAction += 1 # Increment the current action>
      
def executeAction(action):
    if(action["actionType"] == "moveTCP"):
        UR5.moveTCPandWait(action["move"], action["type"])
        
    if(action["actionType"] == "gripper"):
        gripper.endEffector(action["mode"], action.get("position"), action.get("force"))
        
    if(action["actionType"] == "vision"):
        pass

def stopAutoRobot():
    UR5.stop()  

def priorMove():
    global currentAction
    moving = False if len(UR5.getAllTargets()) == 0 else True
    
    if currentAction == 1:
        UR5.home()
        window.controlMenu.testMenu.buttonBack.setEnabled(False)
        window.controlMenu.buttonTest.setEnabled(True)
        window.controlMenu.buttonWork.setEnabled(True)
        currentAction = 0
        return   
        
    if currentAction > 0 and not moving:
        currentAction -= 1
        singleAction(actions[currentAction-1])

def nextMove():
    global currentAction
    moving = False if len(UR5.getAllTargets()) == 0 else True
    print("Current action: ", currentAction)
    if currentAction < len(actions) and not moving:
        singleAction(actions[currentAction])
        # executeAction(actions[currentAction-1])
        currentAction += 1
    
    if currentAction == len(actions):
        window.controlMenu.testMenu.buttonNext.setEnabled(False)
    
    window.controlMenu.buttonTest.setEnabled(False)
    window.controlMenu.buttonWork.setEnabled(False)

def updateUI():
    colors = objRec.get_colors()
    print("Colors: ", colors)
    window.dropdownStacker.cellDisplay.update_colors(colors)
    
def reset():
    global currentAction
    global actions
    global autoThread
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
    homeActions.append({"actionType": "home"})
    
    homingThread = ExcecuteSeriesThread(homeActions, UR5, gripper) # Create a thread to execute the actions
    homingThread.start() # Start the thread
    homingThread.join()
    
    updateUI()
    generateMoves()
    window.controlMenu.buttonTest.setEnabled(True)
    window.controlMenu.buttonWork.setEnabled(True)

def onChangeToAutoMode():
    window.dropdownStacker.calibrator.startCal.setEnabled(False) # Disable the calibrator button
    
def onChangeToCalMode():
    window.dropdownStacker.calibrator.startCal.setEnabled(True) # Enable the calibrator button

def posInBase(frame: np.array, pose: Pose):
    base = pose.matrix
    return  inv(base) @ frame # The position of the frame in the base frame

def getGlobalPos(frame: np.array, pose: Pose):
    return pose.getGlobalPos() @ frame # The position of the frame in the global frame

def baseFrameChanged(index):
    global currentCalibrationFrame
    currentCalibrationFrame = baseFrames[index]
    updateUIPosition()
    print("Base frame changed to:", currentCalibrationFrame.name)
    
def calibrateRobot():
    global calibrationActive
    window.controlMenu.testMenu.buttonNext.setEnabled(False)
    window.controlMenu.testMenu.buttonBack.setEnabled(False)
    window.controlMenu.testMenu.buttonReset.setEnabled(False)
    calibrationActive = True

# the frame you want in the list remeber to change every thing 
replace = Pose(len(Frames)+1,"Dropoff", np.array([[1, 0, 0, 0.5],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]]),"Dropoff first frame for the robot Date: 04-04-2025",Frames[1])
  

# skal listen moves
def stopCalibration():
    global calibrationActive
    window.controlMenu.testMenu.buttonNext.setEnabled(True)
    window.controlMenu.testMenu.buttonBack.setEnabled(True)
    window.controlMenu.testMenu.buttonReset.setEnabled(True)
    calibrationActive = False

def translateFrame(axis, value):
    try:
        value = float(value)
    except ValueError:
        print("Invalid value:", value)
        return
    #print("Translating along:", axis, "by:", value)
    tempFrame = Pose(99, "temp", posInBase(UR5.getCurrentPos(), currentCalibrationFrame), base = currentCalibrationFrame) # The current position of the robot
    
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
    
    tempFrame = Pose(99, "temp", posInBase(UR5.getCurrentPos(), currentCalibrationFrame), base = currentCalibrationFrame) # The current position of the robot
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
        if not calibrationActive:
            updateUIPosition() # Update the current pose in the UI
            
        currentMode = window.controlMenu.getCurrentMode() 
        # if currentMode == "auto":
        #     if len(UR5.getAllTargets()) == 0 or len(actions) == 0:
        #         window.controlMenu.setProgress(0,0)
        #         window.controlMenu.setCurrentTarget("None")
        #         window.controlMenu.setNextTarget("None")
        #         continue
        #     currentAutoMove = len(actions) - len(UR5.getAllTargets())  
        #     window.controlMenu.setProgress(currentAutoMove + 1, len(actions))
        #     window.controlMenu.setCurrentTarget(actions[currentAutoMove]["name"])
        #     if(currentAutoMove + 1) >= len(actions):
        #         window.controlMenu.setNextTarget("None")
        #         continue
        #     window.controlMenu.setNextTarget(actions[currentAutoMove+1]["name"])
        # else:
        if(currentAction == 0):
            window.controlMenu.setProgress(0,len(actions))
            window.controlMenu.setCurrentTarget("None")
            window.controlMenu.setNextTarget("None")
            continue
        currentProgress = currentAction + 1 if currentMode == "auto" else currentAction
        window.controlMenu.setProgress(currentProgress, len(actions))
        
        currentTarget = actions[currentAction]["name"] if currentMode == "auto" else actions[currentAction-1]["name"]
        nextTarget = actions[currentAction+1]["name"] if currentMode == "auto" else actions[currentAction]["name"]
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
#showFramesInList()
def main():
    
    generateCellFrames()# If you want to generate other cells on comentar this code (2)
    saveList()# (3)
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
    window.dropdownStacker.calibrator.setTranslateX(translateFrame, "x") # Set the function to be called when the button is pressed
    window.dropdownStacker.calibrator.setTranslateY(translateFrame, "y") # Set the function to be called when the button is pressed
    window.dropdownStacker.calibrator.setTranslateZ(translateFrame, "z") # Set the function to be called when the button is pressed
    window.dropdownStacker.calibrator.setRotate(rotateFrame)
    
    window.dropdownStacker.calibrator.dropdown.addItems(map(lambda base: base.name, baseFrames)) # Add the base frames to the dropdown menu
    window.dropdownStacker.calibrator.setFunctionChangeBase(baseFrameChanged) # Connect the dropdown menu to the function
    
    updateUI()
    window.controlMenu.testMenu.buttonBack.setEnabled(False) # Disable the back button
    window.runUI() # Run the GUI
    
 # Show the frames in the list
main()







