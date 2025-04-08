from time import sleep
from rtde_stuff.rtde_com import RTDEConnection

"""
This function can actuate the gripper, the gripper can operate in 3 different modes.

Force, based on current, no specific position threshold
Force, based on current, fails if force is not reached within position threshold
Position, based on persentage, 0 is fully closed, 100 is fully open.

A continuous current monitoring ensures that the current will never exeed 80% of the maximum rating

This function is blocking and will only exit when the gripper have executed all its actions specified in the parameters

This function expects that the following global vars exist

tool_current should holdt the tool current in mA datatype is 64-bit floating point (double) RTDE name is tool_output_current
"""
class GripperController:

    def __init__(self, arm:RTDEConnection):
        self.arm = arm
    
    def endEffector(self, mode:str, position:int = None, force:int = None) -> bool:
        """
        mode = "force" = Force, based on current, no specific position threshold\n
        mode = "force_thresh" = Force, based on current, fails if force is not reached within position threshold\n
        mode = "position" = Position, based on persentage, 0 is fully closed, 100 is fully open\n
        position = 0-100 = The position that the gripper should obtain, 0 is fully closed, 100 is fully open. If mode is "force_thresh" the position will be used as the expected end position.\n
        force = 0-100, the target force that the gripper should apply when mode = "force" or "force_thresh"
        """
        speed = 10 # In percent pr. sec.
        pos_out # Global vars to get the tool current and set the tool output to the robot
        servo_at_0 = 30 # When robot receives this number, the gripper is fully closed
        servo_at_100 = 75 # When robot receives this number, the gripper is fully open
        update_freq = 0.1 # The refresh rate of the gripper pos and force measurement in seconds.
        
        
        if(mode == "force"):
            if(0 <= force <= 100):
                while(abs(actual_force - force) <= 10):
                    tool_current = self.getToolCurrent()
                    actual_force = scaleWithParams(tool_current, 0, 600, 0, 100)
                    if(actual_force > 80):
                        return False
                    
                    actual_pos = scaleWithParams(pos_out, servo_at_0, servo_at_100, 0, 100)
                    new_pos = actual_pos - (speed * update_freq)
                    pos_out = scaleWithParams(new_pos, 0, 100, servo_at_0, servo_at_100)
                    
                    sleep(update_freq)
            else:
                raise ValueError(f"Force out of range: force = {force} Should be 0 too 100")
            return True

        if(mode == "force_thresh"):
            if(0 <= force <= 100 and 0 <= position <= 100):
                while(abs(actual_force - force) <= 10):
                    tool_current = self.getToolCurrent()
                    actual_force = scaleWithParams(tool_current, 0, 600, 0, 100)
                    if(actual_force > 80):
                        return False
                    
                    actual_pos = scaleWithParams(pos_out, servo_at_0, servo_at_100, 0, 100)
                    new_pos = actual_pos - (speed * update_freq)
                    pos_out = scaleWithParams(new_pos, 0, 100, servo_at_0, servo_at_100)
                    
                    if(new_pos < position + 10):
                        return False
                
                    sleep(update_freq)
            else:
                raise ValueError(f"Parameter out of range: force = {force} Should be 0 too 100: position = {position} Should be 0 too 100")
            return True

        if(mode == "position"):
            if(0 <= position <= 100):
                while(actual_pos > position):
                    tool_current = self.getToolCurrent()
                    actual_force = scaleWithParams(tool_current, 0, 600, 0, 100)
                    if(actual_force > 80):
                        return False
                
                    actual_pos = scaleWithParams(pos_out, servo_at_0, servo_at_100, 0, 100)
                    new_pos = actual_pos - (speed * update_freq)
                    pos_out = scaleWithParams(new_pos, 0, 100, servo_at_0, servo_at_100)
                    
                    sleep(update_freq)
            else:
                raise ValueError(f"Position out of range: position = {position} Should be 0 too 100")
            return True

        raise ValueError(f"Unknown mode: {mode}")  

def scaleWithParams(x, in_min, in_max, out_min, out_max):
    """
    Maps the input x that has a range from in_min to in_max and returns it in the range out_min to out_max
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min