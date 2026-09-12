#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

from types import SimpleNamespace

import ntcore
import pytest
from wpiutil import Color
from wpilib.testing.robot_tests import *


def test_color_sensor_telemetry(robot, control):
    # I2C hardware is unavailable in simulation; supply known sensor readings.
    robot.color_sensor = SimpleNamespace(
        get_color=lambda: Color(0.143, 0.427, 0.429),
        get_ir=lambda: 123,
        get_proximity=lambda: 456,
        get_raw_color=lambda: SimpleNamespace(red=10, green=20, blue=30, ir=40),
    )
    nt = ntcore.NetworkTableInstance.get_default()

    with control.run_robot():
        control.step_timing(seconds=0.2, autonomous=False, enabled=False)
        for key, value in (("Red", 0.143), ("Green", 0.427), ("Blue", 0.429)):
            assert nt.get_entry(f"/Telemetry/{key}").get_double(-1) == pytest.approx(
                value, abs=1 / 4096
            )
        for key, value in (
            ("IR", 123),
            ("Proximity", 456),
            ("Raw Red", 10),
            ("Raw Green", 20),
            ("Raw Blue", 30),
            ("Raw IR", 40),
        ):
            assert nt.get_entry(f"/Telemetry/{key}").get_integer(-1) == value
