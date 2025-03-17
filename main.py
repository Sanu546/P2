import sys
from rtde_stuff.rtde_com import RTDEConnection
import time
import numpy as np

UR5 = RTDEConnection() # Connnect to the UR5 robot

def main():
    #Example code
    print("Ready to execute commands")
    time.sleep(4)
    UR5.moveJoint([np.radians(-41.62), np.radians(-66.38), np.radians(-110.76), np.radians(56.17), np.radians(93.86), np.radians(38.53)]) # Move to a specific position
    UR5.moveTCP([0.29, -0.25, 0.50, 0.02, 2.8, -1.362]) # Move to a specific position
    print("Move added to queue")
    UR5.moveTCPandWait([0.40, -0.55, 0.20, 0.50, 1.5, -1.362], "l") # Move to a specific position
    print(f"Moved to final position({str(UR5.getCurrentPos())})")
    UR5.setToolPos(69)
    time.sleep(2)
    
    
    #Stuff so you can ctrl+c to exit the program
    while True:
        pass
    #UR5.kill()# Kill the connection to the robot, so the server thread stops running

#stuff so you can ctrl+c to exit the program
try:
    main()
    
except KeyboardInterrupt:
    print("Disconnected from robot")
    UR5.kill()
    sys.exit()





