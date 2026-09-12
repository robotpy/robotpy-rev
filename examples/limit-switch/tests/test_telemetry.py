#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import ntcore
import rev
from wpilib.testing.robot_tests import *


def test_limit_switch_telemetry_and_tuning(robot, control):
    nt = ntcore.NetworkTableInstance.get_default()

    with control.run_robot():
        control.step_timing(seconds=0.2, autonomous=False, enabled=True)
        for key in ("Forward Limit Switch", "Reverse Limit Switch"):
            assert nt.get_topic(f"/Telemetry/{key}").get_type_string() == "boolean"

        # Exercise each direction independently, including re-enabling a limit.
        for forward, reverse in ((False, True), (True, False), (True, True)):
            nt.get_entry("/Tunables/Forward Limit Enabled").set_boolean(forward)
            nt.get_entry("/Tunables/Reverse Limit Enabled").set_boolean(reverse)
            control.step_timing(seconds=0.2, autonomous=False, enabled=True)
            assert robot.prev_forward_limit_enabled is forward
            assert robot.prev_reverse_limit_enabled is reverse
            limits = robot.motor.config_accessor.limit_switch
            for enabled, behavior in (
                (forward, limits.get_forward_limit_switch_trigger_behavior()),
                (reverse, limits.get_reverse_limit_switch_trigger_behavior()),
            ):
                assert behavior == (
                    rev.LimitSwitchConfig.Behavior.STOP_MOVING_MOTOR
                    if enabled
                    else rev.LimitSwitchConfig.Behavior.KEEP_MOVING_MOTOR
                )
