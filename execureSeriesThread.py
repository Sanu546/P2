import threading
from resetException import ResetException


class ExcecuteSeriesThread(threading.Thread):
    stateName = None
    stateNextName = None
    stateIndex = 0
    cellAdded = False
    def __init__(self, series, robot, gripper, resetEvent: threading.Event = None, updateUI = None):
        
        super(ExcecuteSeriesThread, self).__init__()
        self.daemon = True
        self.series = series
        self.robot = robot
        self.gripper = gripper
        self.resetEvent = resetEvent
        self.updateUI = updateUI

    
    def getState(self):
        return self.stateName, self.stateNextName, self.stateIndex
    
    def addToSeries(self, actions):
        for action in actions:
            self.series.append(action)
            
    
    def run(self):
        try: 
            for index, action in enumerate(self.series):
                if self.resetEvent != None and self.resetEvent.is_set():
                    self.resetEvent.clear()
                    self.stateName = None
                    self.stateNextName = None
                    self.stateIndex = None
                    raise ResetException
                
                if(action["actionType"] == "home"):
                    self.stateName = None
                    self.stateNextName = None
                    self.stateIndex = None
                    self.robot.home()
                    
                if(action["actionType"] == "moveTCP"):
                    self.stateName = action["name"]
                    self.stateNextName = self.series[index + 1]["name"] if index + 1 < len(self.series) else None
                    self.stateIndex = index
                    self.robot.moveTCPandWait(action["move"], action["type"])
                    
                if(action["actionType"] == "gripper"):
                    self.stateName = action["name"]
                    self.stateNextName = self.series[index + 1]["name"] if index + 1 < len(self.series) else None
                    self.stateIndex = index
                    self.gripper.endEffector(action["mode"], action.get("position"), action.get("force"))
                    
                if(action["actionType"] == "setJoints"):
                    self.stateName = action["name"]
                    self.stateNextName = self.series[index + 1]["name"] if index + 1 < len(self.series) else None
                    self.stateIndex = index
                    self.robot.moveJointandWait(action["move"])
                
                if(action["actionType"] == "vision"):
                    self.updateUI()
                
        except ResetException:
            pass
        
        except KeyError:
            print("Invalid ket for action")