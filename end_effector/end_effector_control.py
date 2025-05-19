"""
This function can actuate the gripper, the gripper can operate in 3 different modes.
Force, based on current, no specific position threshold
Force, based on current, fails if force is not reached within position threshold
Position, based on persentage, 0 is fully closed, 100 is fully open.
"""
from time import sleep
from rtde_stuff.rtde_com import RTDEConnection
import end_effector.PWMsignal as PWMsignal

class GripperController:
    """
    A continuous current monitoring ensures that the current 
    will never exeed 80% of the maximum rating
    
    This function is blocking and will only exit when the gripper have executed all its actions
    specified in the parameters
    """
    # Global constant for all instances of this class
    SPEED = 10 # In percent pr. sec.
    UPDATE_INTERVAL = 0.1 # The refresh rate of the gripper pos and force measurement in seconds.


    def __init__(self, arm:RTDEConnection):
        # Local variables that follow each instance of the class
        self.arm = arm # Reference to the particular robot that the gripper is mounted on
        self.posOut = 0 # Store the current position between endEffector actions
        

    def endEffector(self, mode:str, endPosition:int = None, force:int = None) -> bool:
        """
        mode = "force" = Force, based on current, no specific position threshold\n
        mode = "force_thresh" = Force, based on current, 
        fails if force is not reached within position threshold\n
        mode = "position" = Position, based on persentage, 0 is fully closed, 100 is fully open\n
        position = 0-100 = The position that the gripper should obtain, 0 is fully closed,
        100 is fully open. If mode is "force_thresh"
        the position will be used as the expected end position.\n
        force = 0-100, the target force that the gripper should apply
        when mode = "force" or "force_thresh"
        """
        servoAt0 = 6 # When robot receives this number, the gripper is fully closed
        servoAt100 = 3 # When robot receives this number, the gripper is fully open
        defaultPanicPos = 4.5

        actualPos = scaleWithParams(self.posOut, servoAt0, servoAt100, 0, 100) # Get actual pos from instance specific variable


        print(f"Actuating gripper, mode = {mode}, force = {force}, position = {endPosition}")

        if mode == "force":
            if 0 <= force <= 100:
                while abs(actualForce - force) <= 10:
                    toolCurrent = self.arm.getToolCurrent()
                    actualForce = scaleWithParams(toolCurrent, 0, 600, 0, 100)
                    if actualForce > 80:
                        PWMsignal.pwm(defaultPanicPos)
                        return False

                    actualPos -= (GripperController.SPEED * GripperController.UPDATE_INTERVAL)
                    self.posOut = scaleWithParams(actualPos, 0, 100, servoAt0, servoAt100)
                    PWMsignal.pwm(self.posOut)

                    sleep(GripperController.UPDATE_INTERVAL)
            else:
                raise ValueError(f"Force out of range: force = {force} Should be 0 too 100")
            return True

        if mode == "force_thresh":
            if(0 <= force <= 100 and 0 <= endPosition <= 100):
                while abs(actualForce - force) <= 10:
                    toolCurrent = self.arm.getToolCurrent()
                    actualForce = scaleWithParams(toolCurrent, 0, 600, 0, 100)
                    if actualForce > 80:
                        PWMsignal.pwm(self.posOut)
                        return False

                    actualPos -= (GripperController.SPEED * GripperController.UPDATE_INTERVAL)
                    self.posOut = scaleWithParams(actualPos, 0, 100, servoAt0, servoAt100)
                    PWMsignal.pwm(self.posOut)

                    if actualPos < endPosition + 10:
                        PWMsignal.pwm(defaultPanicPos)
                        return False

                    sleep(GripperController.UPDATE_INTERVAL)
            else:
                raise ValueError(f"Parameter out of range: force = {force} Should be 0 too 100: position = {endPosition} Should be 0 too 100")
            return True

        if mode == "position":
            if endPosition == "lidopen":
                PWMsignal.setServoPos("lidopen")
                sleep(GripperController.UPDATE_INTERVAL)
            elif endPosition == "lidclose":
                PWMsignal.setServoPos("lidclose")
                sleep(GripperController.UPDATE_INTERVAL)
            elif endPosition == "blockopen":        
                PWMsignal.setServoPos("blockopen")
                sleep(GripperController.UPDATE_INTERVAL)
            elif endPosition == "blockclose":   
                PWMsignal.setServoPos("blockclose")
                sleep(GripperController.UPDATE_INTERVAL)
            else:
                raise ValueError(f"Position out of range: position = {endPosition} Should be 0 too 100")
            return True

        raise ValueError(f"Unknown mode: {mode}")

def scaleWithParams(x, inMin, inMax, outMin, outMax):
    """
    Maps the input x that has a range from in_min to in_max 
    and returns it in the range out_min to out_max
    """
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
