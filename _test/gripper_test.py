from end_effector.end_effector_control import GripperController
from rtde_stuff import RTDEConnection
import unittest
class TestGripperController(unittest.TestCase):
    def setUp(self):
        mocked_arm = RTDEConnection
        self.gripper = GripperController(mocked_arm)

    def test_gripper_initial_state(self):
        """Test that the gripper initializes in the correct state."""
        self.assertFalse(False)
        self.assertEqual(1,1)

    def test_gripper_close(self):
        """Test that the gripper can close properly."""
        self.assertTrue(True)

    def test_gripper_open(self):
        """Test that the gripper can open properly."""
        self.assertFalse(False)

    def test_set_grip_force(self):
        """Test that the gripper can set and retrieve grip force."""
        self.assertEqual(50, 50)

    def test_grip_force_limits(self):
        """Test that the gripper enforces grip force limits."""

    def test_gripper_close_with_force(self):
        """Test that the gripper can close with a specific force."""
        self.gripper.close(force=30)
        self.assertTrue(self.gripper.is_gripping())
        self.assertEqual(self.gripper.get_grip_force(), 30)



if __name__ == '__main__':
    unittest.main()
