import threading

class ExcecuteThread(threading.Thread):
    def __init__(self, action, robot, gripper, window):
        super(ExcecuteThread, self).__init__()
        self.daemon = True  # Set the thread as a daemon thread
        self.action = action
        self.robot = robot
        self.gripper = gripper
        self.window = window

    def run(self):
        if(self.action["actionType"] == "home"):
            self.robot.home()
            
        if(self.action["actionType"] == "moveTCP"):
            self.robot.moveTCPandWait(self.action["move"], self.action["type"])
            self.window.controlMenu.testMenu.buttonNext.setEnabled(True)
            self.window.controlMenu.testMenu.buttonReset.setEnabled(True)
            self.window.controlMenu.testMenu.buttonBack.setEnabled(True)
        
        if(self.action["actionType"] == "gripper"):
            self.gripper.endEffector(self.action["mode"], self.action.get("position"), self.action.get("force"))
            self.window.controlMenu.testMenu.buttonNext.setEnabled(True)
            self.window.controlMenu.testMenu.buttonReset.setEnabled(True)
            self.window.controlMenu.testMenu.buttonBack.setEnabled(True)
        
        if(self.action["actionType"] == "vision"):
            pass
        
        if(self.action["actionType"] == "setJoints"):
            self.robot.moveJointandWait(self.action["move"])
            self.window.controlMenu.testMenu.buttonNext.setEnabled(True)
            self.window.controlMenu.testMenu.buttonReset.setEnabled(True)
            self.window.controlMenu.testMenu.buttonBack.setEnabled(True)
        
        
        