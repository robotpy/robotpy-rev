import wpilib

import rev


def test_set_velocity():
    a301 = rev.A301(wpilib.CANPort.CAN_S0)
    a301.set_velocity(12.34)


def test_set_relative_position():
    a301 = rev.A301(wpilib.CANPort.CAN_S1, 1)
    a301.set_relative_position_with_speed(12.34, 350.0)
