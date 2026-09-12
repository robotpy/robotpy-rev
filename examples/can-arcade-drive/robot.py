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
        # The example below initializes four brushless motors with CAN IDs
        # 1, 2, 3, 4. Change these parameters to match your setup
        self.left_lead_motor = rev.SparkMax(
            wpilib.CANPort.CAN_S0, 1, rev.SparkLowLevel.MotorType.BRUSHLESS
        )
        self.right_lead_motor = rev.SparkMax(
            wpilib.CANPort.CAN_S0, 3, rev.SparkLowLevel.MotorType.BRUSHLESS
        )
        self.left_follow_motor = rev.SparkMax(
            wpilib.CANPort.CAN_S0, 2, rev.SparkLowLevel.MotorType.BRUSHLESS
        )
        self.right_follow_motor = rev.SparkMax(
            wpilib.CANPort.CAN_S0, 4, rev.SparkLowLevel.MotorType.BRUSHLESS
        )

        # Passing in the lead motors into DifferentialDrive allows any
        # commmands sent to the lead motors to be sent to the follower motors.
        self.drivetrain = wpilib.DifferentialDrive(
            self.left_lead_motor, self.right_lead_motor
        )
        self.joystick = wpilib.Joystick(0)

        # Create new SPARK MAX configuration objects. These will store the
        # configuration parameters for the SPARK MAXes that we will set below.
        self.global_config = rev.SparkMaxConfig()
        self.right_leader_config = rev.SparkMaxConfig()
        self.left_follower_config = rev.SparkMaxConfig()
        self.right_follower_config = rev.SparkMaxConfig()

        # Apply the global config and invert since it is on the opposite side
        self.right_leader_config.apply(self.global_config).inverted(True)

        # Apply the global config and set the leader SPARK for follower mode
        self.left_follower_config.apply(self.global_config).follow(self.left_lead_motor)

        # Apply the global config and set the leader SPARK for follower mode
        self.right_follower_config.apply(self.global_config).follow(
            self.right_lead_motor
        )

        # Apply the configuration to the SPARKs.
        #
        # RESET_SAFE_PARAMETERS is used to get the SPARK MAX to a known state.
        # This is useful in case the SPARK MAX is replaced.
        #
        # PERSIST_PARAMETERS is used to ensure the configuration is not lost when
        # the SPARK MAX loses power. This is useful for power cycles that may occur
        # mid-operation.
        self.left_lead_motor.configure(
            self.global_config,
            rev.ResetMode.RESET_SAFE_PARAMETERS,
            rev.PersistMode.PERSIST_PARAMETERS,
        )
        self.left_follow_motor.configure(
            self.left_follower_config,
            rev.ResetMode.RESET_SAFE_PARAMETERS,
            rev.PersistMode.PERSIST_PARAMETERS,
        )
        self.right_lead_motor.configure(
            self.right_leader_config,
            rev.ResetMode.RESET_SAFE_PARAMETERS,
            rev.PersistMode.PERSIST_PARAMETERS,
        )
        self.right_follow_motor.configure(
            self.right_follower_config,
            rev.ResetMode.RESET_SAFE_PARAMETERS,
            rev.PersistMode.PERSIST_PARAMETERS,
        )

    def teleop_periodic(self):
        # Drive with arcade style
        self.drivetrain.arcade_drive(-self.joystick.get_y(), self.joystick.get_x())


if __name__ == "__main__":
    wpilib.run(Robot)
