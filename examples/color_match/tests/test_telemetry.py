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


def test_detected_color_telemetry(robot, control):
    # Supply a deterministic I2C reading, keeping the color matcher real.
    robot.color_sensor = SimpleNamespace(get_color=lambda: Color(0.143, 0.427, 0.429))
    nt = ntcore.NetworkTableInstance.get_default()

    with control.run_robot():
        control.step_timing(seconds=0.2, autonomous=False, enabled=False)
        # Color rounds its channels to 12-bit precision.
        for key, value in (("Red", 0.143), ("Green", 0.427), ("Blue", 0.429)):
            assert nt.get_entry(f"/Telemetry/{key}").get_double(-1) == pytest.approx(
                value, abs=1 / 4096
            )
        assert nt.get_entry("/Telemetry/Confidence").get_double(-1) == pytest.approx(1)
        assert nt.get_entry("/Telemetry/Detected Color").get_string("") == "Blue"
