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
        # The example below initializes four brushless motors with CAN IDs
        # 1, 2, 3, 4. Change these parameters to match your setup
        self.leftLeadMotor = rev.SparkMax(1, rev.SparkMax.MotorType.kBrushless)
        self.rightLeadMotor = rev.SparkMax(3, rev.SparkMax.MotorType.kBrushless)
        self.leftFollowMotor = rev.SparkMax(2, rev.SparkMax.MotorType.kBrushless)
        self.rightFollowMotor = rev.SparkMax(4, rev.SparkMax.MotorType.kBrushless)

        # Passing in the lead motors into DifferentialDrive allows any
        # commmands sent to the lead motors to be sent to the follower motors.
        self.driveTrain = DifferentialDrive(self.leftLeadMotor, self.rightLeadMotor)
        self.joystick = wpilib.Joystick(0)

        # Create new SPARK MAX configuration objects. These will store the
        # configuration parameters for the SPARK MAXes that we will set below.
        self.globalConfig = rev.SparkMaxConfig()
        self.rightLeaderConfig = rev.SparkMaxConfig()
        self.leftFollowerConfig = rev.SparkMaxConfig()
        self.rightFollowerConfig = rev.SparkMaxConfig()

        # Apply the global config and invert since it is on the opposite side
        self.rightLeaderConfig.apply(self.globalConfig).inverted(True)

        # Apply the global config and set the leader SPARK for follower mode
        self.leftFollowerConfig.apply(self.globalConfig).follow(self.leftLeadMotor)

        # Apply the global config and set the leader SPARK for follower mode
        self.rightFollowerConfig.apply(self.globalConfig).follow(self.rightLeadMotor)

        # Apply the configuration to the SPARKs.
        #
        # kResetSafeParameters is used to get the SPARK MAX to a known state. This
        # is useful in case the SPARK MAX is replaced.
        #
        # kPersistParameters is used to ensure the configuration is not lost when
        # the SPARK MAX loses power. This is useful for power cycles that may occur
        # mid-operation.
        self.leftLeadMotor.configure(
            self.globalConfig,
            rev.ResetMode.kResetSafeParameters,
            rev.PersistMode.kPersistParameters,
        )
        self.leftFollowMotor.configure(
            self.leftFollowerConfig,
            rev.ResetMode.kResetSafeParameters,
            rev.PersistMode.kPersistParameters,
        )
        self.rightLeadMotor.configure(
            self.rightLeaderConfig,
            rev.ResetMode.kResetSafeParameters,
            rev.PersistMode.kPersistParameters,
        )
        self.rightFollowMotor.configure(
            self.rightFollowerConfig,
            rev.ResetMode.kResetSafeParameters,
            rev.PersistMode.kPersistParameters,
        )

    def teleopPeriodic(self):
        # Drive with arcade style
        self.driveTrain.arcadeDrive(-self.joystick.getY(), self.joystick.getX())


if __name__ == "__main__":
    wpilib.run(Robot)
