import sys
from rtde_stuff.rtde_com import RTDEConnection
import time

UR5 = RTDEConnection() # Connnect to the UR5 robot

def main():
    time.sleep(6)
    UR5.moveToTCP([0.29, -0.25, 0.50, 0.02, 2.8, -1.362]) # Move to a specific position
    print(f"Moved to position({str(UR5.getCurrentPos())})")
    time.sleep(2)
    UR5.moveToTCP([0.43, -0.35, 0.50, 0.50, 1.5, -1.362]) # Move to a specific position
    print(f"Moved to final position({str(UR5.getCurrentPos())})")
    time.sleep(2)
    UR5.kill()


try:
    main()
    
except KeyboardInterrupt:
    print("Disconnected from robot")
    UR5.kill()
    sys.exit()





