#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import ntcore
import pytest
import rev
from wpilib.simulation import JoystickSim
from wpilib.testing.robot_tests import *


def test_velocity_pid_telemetry_and_tuning(robot, control):
    nt = ntcore.NetworkTableInstance.get_default()
    joystick = JoystickSim(robot.joystick)
    joystick.set_axes_available(2)
    joystick.set_y(0.5)

    with control.run_robot():
        control.step_timing(seconds=0.2, autonomous=False, enabled=True)
        for key, default in (
            ("P Gain", 0.1),
            ("I Gain", 1e-4),
            ("D Gain", 0.0),
            ("I Zone", 0.0),
            ("Feed Forward", 0.0),
            ("Min Output", -1.0),
            ("Max Output", 1.0),
        ):
            assert nt.get_topic(f"/Tunables/{key}").get_type_string() == "double"
            assert nt.get_entry(f"/Tunables/{key}").get_double(999) == pytest.approx(
                default
            )
        assert nt.get_topic("/Telemetry/ProcessVariable").get_type_string() == "double"
        assert nt.get_entry("/Telemetry/SetPoint").get_double(-1) == 2850.0

        nt.get_entry("/Tunables/P Gain").set_double(0.25)
        nt.get_entry("/Tunables/D Gain").set_double(0.125)
        control.step_timing(seconds=0.2, autonomous=False, enabled=True)
        assert robot.p_gain == 0.25
        assert robot.d_gain == 0.125
        assert robot.motor.config_accessor.closed_loop.get_p() == pytest.approx(0.25)
        assert robot.motor.config_accessor.closed_loop.get_d() == pytest.approx(0.125)
        assert robot.pid_controller.get_setpoint().get() == 2850.0
        assert (
            robot.pid_controller.get_control_type()
            == rev.SparkBase.ControlType.VELOCITY
        )
