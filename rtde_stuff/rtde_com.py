import sys

sys.path.append("..")

import logging

logging.getLogger().setLevel(logging.INFO)

import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
import threading as th #Import treading to keep the server running in the background
import numpy as np
import util.matrixConversion as mc

class RTDEConnection:
    config_filename = "rtde_stuff/control_loop_configuration.xml"
    killed = False
    stopped = False  
    targets = []
    moving = False
    
    #constructor
    def __init__(self, ipAddress='192.168.56.101', port=30004, startPos=[np.radians(79.260852), np.radians(-110.886718), np.radians(122.292706), np.radians(53.983734), np.radians(85.484271), np.radians(-189.754028)]):
        
        #Establish a connection to the UR robot
        self.con = rtde.RTDE(ipAddress, port)
        self.con.connect()
        print("Connected to robot")
        self.con.get_controller_version()
        
        self.startPos = startPos
        
        #Make recipes from configuration file(The recipes are the data that will be sent to and from the robot)
        self.conf = rtde_config.ConfigFile(self.config_filename)
        self.state_names, self.state_types = self.conf.get_recipe("state")
        self.setPos_names, self.setPos_types = self.conf.get_recipe("setPose")
        self.watchdog_names, self.watchdog_types = self.conf.get_recipe("watchdog")

        #Setup the recipes on the robot
        self.con.send_output_setup(self.state_names, self.state_types)
        self.setPos = self.con.send_input_setup(self.setPos_names, self.setPos_types)
        self.watchdog = self.con.send_input_setup(self.watchdog_names, self.watchdog_types)

        #Initialize the setPose
        self.setPos.input_double_register_24 = 0
        self.setPos.input_double_register_25 = 0
        self.setPos.input_double_register_26 = 0
        self.setPos.input_double_register_27 = 0
        self.setPos.input_double_register_28 = 0
        self.setPos.input_double_register_29 = 0
        self.setPos.input_int_register_25 = 0
        self.setPos.input_int_register_26 = 0
        
        #Initialize the watchdog
        self.watchdog.input_int_register_24 = 0

        #Start data synchronization
        if not self.con.send_start():
            sys.exit()

        program_running = False

        print("Waiting for robot to start program")
        
        #Start a thread to keep the server running
        self.sync_thread = th.Thread(target=self.syncThread)
        self.sync_thread.daemon = True
        self.sync_thread.start()  
        
        while not program_running:
            state = self.con.receive()
            if state.output_int_register_24 == 1:
                program_running = True
         
        self.moveJointandWait(self.startPos)
        print("Robot is in position and ready to receive commands")
    
    def moveTCPandWait(self, position, type="j"):
        position = mc.matrixToAxisAngle(position)
        print(f"moveTCPandWait: position = {position}")
        self.targets.append({"position": position, "joint": False, "type": type})
        while len(self.targets) > 0:
            pass
     
    def moveJointandWait(self, position):
        self.targets.append({"position": position, "joint": True, "type": "j"})
        while len(self.targets) > 0:
            pass

    #Get the current position of the robot
    def getCurrentPos(self):
        state = self.con.receive()
        return mc.axisAngleToMatrix(state.actual_TCP_pose)
    
    def getCurrentTaget(self):
        state = self.con.receive()
        return mc.axisAngleToMatrix(state.target_TCP_pose)
    
    def getAllTargets(self):
        return self.targets
    
    def resume(self):
        self.stopped = False
    
    def stop(self):
        self.stopped = True
        
    def getStatus(self):
        return self.status
    
    def resetRobot(self):
        self.targets = []
        self.stopped = False
    
    def home(self):
        print("Homing robot")
        self.moveJointandWait(self.startPos) 
    
    def isStopped(self):
        return self.stopped
    
    #Keep the server running in the background
    def syncThread(self):
        while not self.killed:
            if len(self.targets) > 0 and not self.stopped: #If there are targets in the queue
                self.status = "running"
                #print("Moving to target")
                target = self.targets[0]
                #print(target)
                moveDone = False
                
                self.setPos.input_int_register_25 = 0 if target["joint"] else 1
                self.setPos.input_int_register_26 = 0 if target["type"] == "j" else 1
                    
                list_to_setPos(self.setPos, target["position"])
                self.con.send(self.setPos)
                self.watchdog.input_int_register_24 = 1
                state = self.con.receive()
                    
                while not moveDone:
                    state = self.con.receive()
                    #print(f"Robot out: {state.output_int_register_24}")
                    if state.output_int_register_24 == 0: 
                        print("Move done")
                        moveDone = True
                        self.watchdog.input_int_register_24 = 0
                            
                    self.con.send(self.watchdog)
                    
                    while state.output_int_register_24 == 0:
                        state = self.con.receive()
                        
                self.targets.pop(0)
            else:
                self.watchdog.input_int_register_24 = 0
                self.status = "idle"
                #state = self.con.receive()
                #print(f"Robot out: {state.output_int_register_24}")
                self.con.send(self.watchdog)
      
    #Kill the connection to the robot and stop the server thread
    def kill(self):
        self.killed = True
        self.sync_thread.join()
        self.con.send_pause()
        self.con.disconnect()
        print("Disconnected from robot")


def setPos_to_list(sp):
    sp_list = []
    for i in range(0, 6):
        iReg = i + 24
        sp_list.append(sp.__dict__["input_double_register_%i" % iReg])
    return sp_list

def list_to_setPos(sp, list):
    for i in range(0, 6):
        iReg = i + 24
        sp.__dict__["input_double_register_%i" % iReg] = list[i]
    return sp
