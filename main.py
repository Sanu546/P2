import sys
from rtde_stuff.rtde_com import RTDEConnection # Connect to the UR5 robot
import time
import numpy as np
from gui.P2_GUI import MainWindow
import vision.objRec as objRec
from pose import Pose
from typing import List
import threading as th
from numpy.linalg import inv
import matrixConversion as mc
import pickle # nyt sanu

UR5 = RTDEConnection() # Connnect to the UR5 robot   

moves = [] # The moves that the robot will make

cellSpacingX = 0.07 # The spacing between the cells in the x direction in meters
cellSpacingY = 0.046 # The spacing between the cells in the y direction in meters

currentMove = 0

clearHeight = -0.05

# List for every frame
Frames: List[Pose] = [
    Pose(1,"UR5", np.array([[1,     0,     0,   0],
                                [0,     1,     0,   0],
                                [0,     0,     1,   0],
                                [0,     0,     0,   1]]),"UR5 first frame for the robot Date: 04-04-2025"),
    Pose(2,"Ramp", np.array([[    -0.999673,    -0.024494,     0.007347,   .201236369], 
    [-0.023483,     0.765548,    -0.642950,  -.657846558],
    [0.010124,    -0.642913,    -0.765873,   .283486816],
    [0.000000,     0.000000,     0.000000,     1.000000 ]]
            ),"Ramp first frame for the robot Date: 04-04-2025")
    
    
    ] # The frames for the robot

# add fram to the list Frames
Frames.append(Pose(len(Frames)+1,"Dropoff", np.array([[1, 0, 0, 0.5],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]]),"Dropoff first frame for the robot Date: 04-04-2025",Frames[1]))


# Give the seachlist a name and id if need to get the specific object you want to use    
def seachlist(name,id = None):
    number = []
    ideList:List[Pose] = []
    
    if id != None: # check if there are id
     for i in range(len(Frames)):
         if  Frames[i].name == name and Frames[i].id == id: 
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
         print(len(ideList))
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

ur5Frame = Pose(4,"UR5", np.array([[1,     0,     0,   0],
                                [0,     1,     0,   0],
                                [0,     0,     1,   0],
                                [0,     0,     0,   1]]),"sdsdsd") # The frame for the UR5 robot


currentCalibrationFrame = ur5Frame # The current calibration frame

calibrationActive = False

# The frame for the ramp
rampFrame = Pose(1,"Ramp", np.array([[    -0.999673,    -0.024494,     0.007347,   .201236369], 
    [-0.023483,     0.765548,    -0.642950,  -.657846558],
    [0.010124,    -0.642913,    -0.765873,   .283486816],
    [0.000000,     0.000000,     0.000000,     1.000000 ]]
),"sdsdsd")

cellFrames: List[Pose] = [] # The frames for the cells

dropOffFrame = Pose(2,"Dropoff", np.array([[1, 0, 0, 0.5],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]]),"sdsdsd", rampFrame) # The frame for the drop off location

baseFrames: List[Pose] = [
    ur5Frame,
    rampFrame,
    ]
# Er den ikke forkte da det skal være realtive første bokse.
def generateCellFrames():
    rampFrame = seachlist("Ramp") # The frame for the ramp
    for i in range(4):  
        for j in range(2):
            Frames.append(Pose(len(Frames)+1,f"Cell [{i}, {j}]", np.array([[    1,     0,     0,   j*cellSpacingX ],
            [0,     1,     0,   i*cellSpacingY ],
            [0,     0,     1,   0 ],
            [0,     0,     0,     1 ]]),"UR5 first frame for the robot Date: 08-04-2025" ,rampFrame, isCell = True, color = "blue")) 
            
# is show every object in the list of frames. Where can se name,id,matrix and description
def showFramesInList():
    print(f"There are {len(Frames)} frames in the list")
    print("============================================================================")
    for i in range(len(Frames)):
        print(f"Frame {i}: {Frames[i].name}")
        print(f"Is cell: {Frames[i].id}")
        print(f"Matrix: ")
        print(Frames[i].matrix)
        print(f"Description: {Frames[i].description}")
        print("============================================================================")
        print("                                                                            ")
        
            

# add every module to the list of frames bliver ikke brugt mere 
def setCellsInList():
    for i in range(8):
        Frames.append(cellFrames[i])

 # Jeg har prøvet her nu  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def           generateMoves():
    for i in range(4):  
        for j in range(2):
            cell = seachlist(f"Cell [{i}, {j}]")
            print(cell.name)# The frame for the cell
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
    window.dropdownStacker.calibrator.startCal.setEnabled(False)
    

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
        window.controlMenu.buttonTest.setEnabled(True)
        window.controlMenu.buttonWork.setEnabled(True)
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
    
    window.controlMenu.buttonTest.setEnabled(False)
    window.controlMenu.buttonWork.setEnabled(False)

def updateUI():
    colors = objRec.get_colors()
    window.dropdownStacker.cellDisplay.update_colors(colors)
    

def resetAuto():
    global currentMove
    global moves
    rampFrame = seachlist("Ramp") # The frame for the ramp sanu 
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
    global currentCalibrationFrame
    currentCalibrationFrame = baseFrames[index]
    print("Base frame changed to:", currentCalibrationFrame.name)
    
def calibrateRobot():
    global calibrationActive
    window.controlMenu.testMenu.buttonNext.setEnabled(False)
    window.controlMenu.testMenu.buttonBack.setEnabled(False)
    window.controlMenu.testMenu.buttonReset.setEnabled(False)
    
    calibrationActive = True

# the frame you want in the list
replace = Pose(len(Frames)+1,"Dropoff", np.array([[1, 0, 0, 0.5],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]]),"Dropoff first frame for the robot Date: 04-04-2025",Frames[1])
def replaceObject(newframe, id = None):
    
       return     

# skal listen moves
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
            if(currentAutoMove + 1) >= len(moves):
                window.controlMenu.setNextTarget("None")
                continue
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
        
        currentPosition = inv(currentCalibrationFrame.getGlobalPos()) @ UR5.getCurrentPos()
        currentRPY =  mc.matrixToRPY(currentPosition)
        window.dropdownStacker.calibrator.setCurrentPose(currentRPY) # Update the current pose in the UI
        time.sleep(0.1)

def saveRampframe():
    # Gem rampFrame til en fil
    with open('calibrationFrame.pkl', "wb") as file:
        pickle.dump(rampFrame, file)  # Gem rampFrame til en fil
    
    # Indlæs rampFrame fra filen (valgfrit, hvis du vil teste indlæsning)
    with open('calibrationFrame.pkl', "rb") as file:
        loaded_rampFrame = pickle.load(file)  # Indlæs rampFrame fra filen
        print("RampFrame loaded successfully:", loaded_rampFrame)

def pmatrix():
    with open('calibrationFrame.pkl', "rb") as file:
        loaded_rampFrame = pickle.load(file)
        print(loaded_rampFrame.matrix)  # Print matrix from loaded rampFrame
        
        
def saveList():   
        with open('Frames.pkl', "wb") as file:
            pickle.dump(Frames, file)  # Save Pose to a file 
        print("Frames saved successfully")
       


def loadList():
        with open('Frames.pkl', "rb") as file:
            return pickle.load(file)  # Load Pose from the file
        
        
window = MainWindow()
progressThread = th.Thread(target=updateProgramProgress)
progressThread.daemon = True

# To replace Frames list and save new  comented out code were (1) and und commented (2) and (3). Ask Santhosh if don't understand
Frames = loadList() # Load the frames from the file (1)
showFramesInList()
def main():
    
    #generateCellFrames()# If you want to generate other cells on comentar this code (2)
    #saveList()# (3)
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







