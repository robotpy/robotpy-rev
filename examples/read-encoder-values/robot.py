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
    # Optionally, if you call the setPositionConversionFactor() method on the
    # encoder and give it a measurement of how far one revolution is, the
    # getVelocity() and getPosition() methods return a scaled output in the
    # units of your choice.
    def robotInit(self):
        # Instantiate SPARK MAX object
        self.motor = rev.CANSparkMax(1, rev.CANSparkMax.MotorType.kBrushless)

        self.motor.restoreFactoryDefaults()
        self.encoder = self.motor.getEncoder()

        self.joystick = wpilib.Joystick(0)

    def teleopPeriodic(self):
        # Set motor output to the joystick's Y-axis
        self.motor.set(self.joystick.getY())

        # Encoder position is read from a CANEncoder object by calling the
        # getPosition() method.
        #
        # getPosition() returns the position of the encoder in units of
        # revolutions (unless overridden)
        wpilib.SmartDashboard.putNumber("Encoder Position", self.encoder.getPosition())

        # Encoder velocity is read from a CANEncoder object by calling the
        # getVelocity() method.
        #
        # getVelocity() returns the position of the encoder in units of
        # revolutions (unless overridden)
        wpilib.SmartDashboard.putNumber("Encoder Velocity", self.encoder.getVelocity())


if __name__ == "__main__":
    wpilib.run(Robot)
