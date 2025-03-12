import sys

sys.path.append("..")

import logging

logging.getLogger().setLevel(logging.INFO)

import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
import threading as th #Import treading to keep the server running in the background


class RTDEConnection:
    config_filename = "rtde_stuff/control_loop_configuration.xml"
    com_active = False 
    killed = False   
    #constructor
    def __init__(self, ip_address='192.168.56.101', port=30004, startPos=[-0.12, -0.43, 0.14, 0, 3.11, 0.04]):
        
        #Establish a connection to the UR robot
        self.con = rtde.RTDE(ip_address, port)
        self.con.connect()
        print("Connected to robot")

        self.con.get_controller_version()

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
        self.setPos.input_double_register_0 = 0
        self.setPos.input_double_register_1 = 0
        self.setPos.input_double_register_2 = 0
        self.setPos.input_double_register_3 = 0
        self.setPos.input_double_register_4 = 0
        self.setPos.input_double_register_5 = 0
        self.setPos.input_int_register_1 = 0

        #Initialize the watchdog
        self.watchdog.input_int_register_0 = 0

        #Start data synchronization
        if not self.con.send_start():
            sys.exit()

        program_running = False

        print("Waiting for robot to start program")

        while not program_running:
            state = self.con.receive()
            if state.output_int_register_0 == 1:
                program_running = True
         
        self.moveToTCP(startPos)
        print("Robot is in position and ready to receive commands")

        #Start a thread to keep the server running
        self.server_thread = th.Thread(target=self.keep_server_running)
        self.server_thread.start()

    def moveToTCP(self, jointArray):
        self.com_active = True

        move_completed = False
        #Save the joint positions to input registers
        list_to_setPos(self.setPos, jointArray)

        #Set the move type to joints
        self.setPos.input_int_register_1 = 0

        #Send the move to the robot
        self.con.send(self.setPos)
        self.watchdog.input_int_register_0 = 1
        while not move_completed:
            #Receive the current state
            state = self.con.receive()

            #Check if the move is completed
            if state.output_int_register_0 == 0:
                move_completed = True
                self.watchdog.input_int_register_0 = 0

            self.con.send(self.watchdog)

        self.com_active = False

    #Get the current position of the robot
    def getCurrentPos(self):
        self.com_active = True
        state = self.con.receive()
        self.com_active = False
        return state.actual_TCP_pose
    
    #Keep the server running in the background
    def keep_server_running(self):
        while not self.killed:
            if not self.com_active:
                    self.con.receive()
                    self.con.send(self.watchdog)
    
    #Kill the connection to the robot and stop the server thread
    def kill(self):
        self.killed = True
        self.server_thread.join()
        self.con.send_pause()
        self.con.disconnect()
        print("Disconnected from robot")



 
def setPos_to_list(sp):
    sp_list = []
    for i in range(0, 6):
        sp_list.append(sp.__dict__["input_double_register_%i" % i])
    return sp_list


def list_to_setPos(sp, list):
    for i in range(0, 6):
        sp.__dict__["input_double_register_%i" % i] = list[i]
    return sp
