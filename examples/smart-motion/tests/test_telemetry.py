#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import ntcore
import pytest
import rev
from wpilib.testing.robot_tests import *


def test_max_motion_telemetry_and_tuning(robot, control):
    nt = ntcore.NetworkTableInstance.get_default()

    with control.run_robot():
        control.step_timing(seconds=0.2, autonomous=False, enabled=True)
        for key, default in (
            ("P Gain", 5e-5),
            ("I Gain", 1e-6),
            ("D Gain", 0.0),
            ("I Zone", 0.0),
            ("Feed Forward", 0.001872),
            ("Min Output", -1.0),
            ("Max Output", 1.0),
            ("Max Velocity", 1500.0),
            ("Max Acceleration", 500.0),
            ("Allowed Closed Loop Error", 0.0),
            ("Set Position", 0.0),
            ("Set Velocity", 0.0),
        ):
            assert nt.get_topic(f"/Tunables/{key}").get_type_string() == "double"
            assert nt.get_entry(f"/Tunables/{key}").get_double(999) == pytest.approx(
                default
            )
        assert nt.get_entry("/Tunables/Mode").get_boolean(False) is True
        for key in ("SetPoint", "Process Variable", "Output"):
            assert nt.get_topic(f"/Telemetry/{key}").get_type_string() == "double"

        for key, value in (
            ("P Gain", 0.25),
            ("D Gain", 0.125),
            ("Max Velocity", 1600.5),
            ("Max Acceleration", 600.5),
            ("Allowed Closed Loop Error", 0.5),
        ):
            nt.get_entry(f"/Tunables/{key}").set_double(value)
        control.step_timing(seconds=0.2, autonomous=False, enabled=True)
        assert robot.p_gain == 0.25
        assert robot.d_gain == 0.125
        assert robot.max_vel == 1600.5
        assert robot.max_acc == 600.5
        assert robot.allowed_err == 0.5
        config = robot.motor.config_accessor.closed_loop
        assert config.get_p() == pytest.approx(0.25)
        assert config.get_d() == pytest.approx(0.125)
        assert config.max_motion.get_cruise_velocity() == pytest.approx(1600.5)
        assert config.max_motion.get_max_acceleration() == pytest.approx(600.5)
        assert config.get_allowed_closed_loop_error() == pytest.approx(0.5)

        for mode, key, setpoint in (
            (True, "Set Velocity", 123.5),
            (False, "Set Position", 4.5),
        ):
            nt.get_entry("/Tunables/Mode").set_boolean(mode)
            nt.get_entry(f"/Tunables/{key}").set_double(setpoint)
            control.step_timing(seconds=0.2, autonomous=False, enabled=True)
            assert nt.get_entry("/Telemetry/SetPoint").get_double(-1) == setpoint
            assert robot.pid_controller.get_setpoint().get() == setpoint
            assert robot.pid_controller.get_control_type() == (
                rev.SparkBase.ControlType.VELOCITY
                if mode
                else rev.SparkBase.ControlType.MAX_MOTION_POSITION_CONTROL
            )
