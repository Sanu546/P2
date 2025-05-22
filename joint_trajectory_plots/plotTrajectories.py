import json
from datetime import datetime

def plotJointTrajectory(UR5, window):
    urState = UR5.getStatus()
    currentMode = window.controlMenu.getCurrentMode()
    
    with open('joint_trajectory_plots/trajectories.json', "r") as openFile:
        plots = json.load(openFile)

    print(plots["plots"])

    plots["plots"].append({
        "num": len(plots["plots"])+1,
        "joint2": [],
        "joint5": []
    })
    
    startTime = datetime.now()
    while urState == "running" and currentMode == "auto":
        joints = UR5.getCurrentJointPos()
        joint2 = joints[1]
        joint5 = joints[4]
        timeDiff = (startTime - datetime.now()).total_seconds()
        plots["plots"][-1]["joint2"].append([timeDiff, joint2])
        plots["plots"][-1]["joint5"].append([timeDiff, joint5])
    
    with open('joint_trajectory_plots/trajectories.json', "w") as openFile:
        json.dump(plots, openFile, indent=4)
