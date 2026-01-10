#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import rev
import wpilib
from wpilib.drive import DifferentialDrive


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        # SPARK MAX controllers are intialized over CAN by constructing a
        # CANSparkMax object
        #
        # The CAN ID, which can be configured using the SPARK MAX Client, is passed
        # as the first parameter
        #
        # The motor type is passed as the second parameter.
        # Motor type can either be:
        #   rev.CANSparkMax.MotorType.kBrushless
        #   rev.CANSparkMax.MotorType.kBrushed
        #
        # The example below initializes two brushless motors with CAN IDs
        # 1 and 2. Change these parameters to match your setup
        self.leftMotor = rev.SparkMax(1, rev.SparkMax.MotorType.kBrushless)
        self.rightMotor = rev.SparkMax(2, rev.SparkMax.MotorType.kBrushless)

        # Configure for factory defaults and invert right side motor
        self.globalConfig = rev.SparkMaxConfig()
        self.rightConfig = self.globalConfig.inverted(True)
        self.leftMotor.configure(
            self.globalConfig,
            rev.ResetMode.kResetSafeParameters,
            rev.PersistMode.kPersistParameters,
        )
        self.rightMotor.configure(
            self.rightConfig,
            rev.ResetMode.kResetSafeParameters,
            rev.PersistMode.kPersistParameters,
        )

        self.driveTrain = DifferentialDrive(self.leftMotor, self.rightMotor)
        self.l_stick = wpilib.Joystick(0)
        self.r_stick = wpilib.Joystick(1)

    def teleopPeriodic(self):
        # Create tank drive
        self.driveTrain.tankDrive(self.l_stick.getY(), self.r_stick.getY())


if __name__ == "__main__":
    wpilib.run(Robot)
