#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import rev
import wpilib


class Robot(wpilib.TimedRobot):
    # This sample program displays the position and velocity of the integrated
    # encoder onto the SmartDashboard.
    #
    # Position is displayed in revolutions (of the motor's axle) and velocity
    # is displayed in revolutions per minute (RPM)
    #
    # Optionally, if you call the position_conversion_factor() method on the
    # encoder config and give it a measurement of how far one revolution is, the
    # get_velocity() and get_position() methods return a scaled output in the
    # units of your choice after configuring the SPARK.
    def robot_init(self):
        # Instantiate SPARK MAX object
        self.motor = rev.SparkMax(0, 1, rev.SparkLowLevel.MotorType.BRUSHLESS)

        self.motor.configure(
            rev.SparkMaxConfig(),
            rev.ResetMode.RESET_SAFE_PARAMETERS,
            rev.PersistMode.NO_PERSIST_PARAMETERS,
        )
        self.encoder = self.motor.get_encoder()

        self.joystick = wpilib.Joystick(0)

    def teleop_periodic(self):
        # Set motor output to the joystick's Y-axis
        self.motor.set(self.joystick.get_y())

        # Encoder position is read from a RelativeEncoder object by calling the
        # get_position() method.
        #
        # get_position() returns the position of the encoder in units of
        # revolutions (unless overridden)
        wpilib.SmartDashboard.put_number(
            "Encoder Position", self.encoder.get_position()
        )

        # Encoder velocity is read from a RelativeEncoder object by calling the
        # get_velocity() method.
        #
        # get_velocity() returns the position of the encoder in units of
        # revolutions (unless overridden)
        wpilib.SmartDashboard.put_number(
            "Encoder Velocity", self.encoder.get_velocity()
        )


if __name__ == "__main__":
    wpilib.run(Robot)
