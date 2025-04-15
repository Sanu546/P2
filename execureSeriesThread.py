import threading
from resetException import ResetException


class ExcecuteSeriesThread(threading.Thread):
    def __init__(self, series, robot, gripper, resetEvent: threading.Event = None ):
        super(ExcecuteSeriesThread, self).__init__()
        self.daemon = True
        self.series = series
        self.robot = robot
        self.gripper = gripper
        self.resetEvent = resetEvent
    
    def run(self):
        try: 
            for action in self.series:
                if self.resetEvent != None and self.resetEvent.is_set():
                    self.resetEvent.clear()
                    raise ResetException
                if(action["actionType"] == "home"):
                    self.robot.home()
                    
                if(action["actionType"] == "moveTCP"):
                    self.robot.moveTCPandWait(action["move"], action["type"])
                    
                if(action["actionType"] == "gripper"):
                    self.gripper.endEffector(action["mode"], action.get("position"), action.get("force"))
                    
                if(action["actionType"] == "vision"):
                    pass
        except ResetException:
            pass