import sys
from rtde_stuff.rtde_com import RTDEConnection
import time
import numpy as np
import matrixConversion as mc
from gui.P2_GUI import MainWindow
import random

UR5 = RTDEConnection() # Connnect to the UR5 robot

def exampleProgram():
    UR5.moveJoint([np.radians(-41.62), np.radians(-66.38), np.radians(-110.76), np.radians(56.17), np.radians(93.86), np.radians(38.53)]) # Move to a specific position
    UR5.moveTCP([0.29, -0.25, 0.50, 0.02, 2.8, -1.362]) # Move to a specific position
    print("Move added to queue")
    UR5.moveTCPandWait([0.40, -0.55, 0.20, 0.50, 1.5, -1.362], "l") # Move to a specific position
    print(f"Moved to final position({str(UR5.getCurrentPos())})")
    UR5.setToolPos(50)
    time.sleep(2)
    


def main():
    #Random number
    num = random.randint(1, 3)
    print(f"Random number: {num}")
    window = MainWindow()
    window.controlMenu.testMenu.setFunctionNext(exampleProgram) # Set the function to be called when the button is pressed
    window.runUI() # Run the GUI
    

#stuff so you can ctrl+c to exit the program
try:
    main()
    
except KeyboardInterrupt:
    print("Disconnected from robot")
    UR5.kill()
    sys.exit()





