import subprocess
import sys

import wpilib

import rev


def test_set_velocity():
    a301 = rev.A301(wpilib.CANPort.CAN_S0)
    a301.set_velocity(12.34)


def test_set_relative_position():
    a301 = rev.A301(wpilib.CANPort.CAN_S1, 1)
    a301.set_relative_position_with_speed(12.34, 350.0)


def test_motioncore_construction_in_fresh_process():
    # Exercise backend initialization at import time. A subprocess isolates a
    # native crash and avoids hiding initialization-order bugs with prior tests.
    result = subprocess.run(
        [
            sys.executable,
            "-X",
            "faulthandler",
            "-c",
            "import rev, wpilib; "
            "rev.A301(wpilib.CANPort.CAN_D0); "
            "rev.A301(wpilib.CANPort.CAN_D1, 1)",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
