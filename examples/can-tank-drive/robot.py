#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import rev
import wpilib


class Robot(wpilib.TimedRobot):
    def __init__(self):
        super().__init__()
        # SPARK MAX controllers are intialized over CAN by constructing a
        # SparkMax object.
        #
        # The CAN bus ID is passed as the first parameter, and the device ID,
        # which can be configured using the SPARK MAX Client, is passed as the
        # second parameter.
        #
        # The motor type is passed as the third parameter.
        # Motor type can either be:
        #   rev.SparkLowLevel.MotorType.BRUSHLESS
        #   rev.SparkLowLevel.MotorType.BRUSHED
        #
        # The example below initializes two brushless motors with CAN IDs
        # 1 and 2. Change these parameters to match your setup
        self.left_motor = rev.SparkMax(
            wpilib.CANPort.CAN_S0, 1, rev.SparkLowLevel.MotorType.BRUSHLESS
        )
        self.right_motor = rev.SparkMax(
            wpilib.CANPort.CAN_S0, 2, rev.SparkLowLevel.MotorType.BRUSHLESS
        )

        # Configure for factory defaults and invert right side motor
        self.global_config = rev.SparkMaxConfig()
        self.right_config = self.global_config.inverted(True)
        self.left_motor.configure(
            self.global_config,
            rev.ResetMode.RESET_SAFE_PARAMETERS,
            rev.PersistMode.PERSIST_PARAMETERS,
        )
        self.right_motor.configure(
            self.right_config,
            rev.ResetMode.RESET_SAFE_PARAMETERS,
            rev.PersistMode.PERSIST_PARAMETERS,
        )

        self.drivetrain = wpilib.DifferentialDrive(self.left_motor, self.right_motor)
        self.l_stick = wpilib.Joystick(0)
        self.r_stick = wpilib.Joystick(1)

    def teleop_periodic(self):
        # Create tank drive
        self.drivetrain.tank_drive(self.l_stick.get_x(), self.r_stick.get_y())


if __name__ == "__main__":
    wpilib.run(Robot)
