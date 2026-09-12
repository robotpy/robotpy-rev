#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import math

from subsystems.drivesubsystem import DriveSubsystem


class FakeGyro:
    def __init__(self, angle_z: float) -> None:
        self.angle_z = angle_z

    def get_angle_z(self) -> float:
        return self.angle_z


def test_get_heading_interprets_onboard_imu_angle_z_as_radians():
    drive = DriveSubsystem.__new__(DriveSubsystem)
    drive.gyro = FakeGyro(math.pi / 2)

    assert drive.get_heading() == 90
