#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# Copyright (c) 2017-2018 FIRST. All Rights Reserved.
# Open Source Software - may be modified and shared by FRC teams. The code
# must be accompanied by the FIRST BSD license file in the root directory of
# the project.
# ----------------------------------------------------------------------------

import rev
import wpilib
from wpilib.drive import DifferentialDrive


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        # Create motors
        self.motor = rev.CANSparkMax(0, rev.MotorType.kBrushless)

        # You must call getPIDController() on an existing CANSparkMax or
        # SparkMax object to fully use PID functionality
        self.pidController = self.motor.getPIDController()

        # Instantiate built-in encoder to display position
        self.encoder = self.motor.getEncoder()

        # PID Coefficents and Controller Output Range
        self.coeff = {
            'p': 0.1,
            'i': 1e-4,
            'd': 0,
            'iz': 0,
            'ff': 0
        }
        self.kMinOutput = -1
        self.kMaxOutput = 1

        # The restoreFactoryDefaults() method can be used to reset the
        # configuration parameters in the SPARK MAX to their factory default
        # state. If no argument is passed, these parameters will not persist
        # between power cycles
        self.motor.restoreFactoryDefaults()

        # Set PID Coefficents
        self.pidController.setP(self.coeff['p'])
        self.pidController.setI(self.coeff['i'])
        self.pidController.setD(self.coeff['d'])
        self.pidController.setIZone(self.coeff['iz'])
        self.pidController.setFF(self.coeff['ff'])
        self.pidController.setOutputRange(self.kMinOutput, self.kMaxOutput)

        # Push PID Coefficients to SmartDashboard
        wpilib.SmartDashboard.putNumber("P Gain", self.coeff['p'])
        wpilib.SmartDashboard.putNumber("I Gain", self.coeff['i'])
        wpilib.SmartDashboard.putNumber("D Gain", self.coeff['d'])
        wpilib.SmartDashboard.putNumber("I Zone", self.coeff['iz'])
        wpilib.SmartDashboard.putNumber("Feed Forward", self.coeff['ff'])
        wpilib.SmartDashboard.putNumber("Min Output", self.kMinOutput)
        wpilib.SmartDashboard.putNumber("Max Output", self.kMaxOutput)
        wpilib.SmartDashboard.putNumber("Set Rotations", 0)

    def teleopPeriodic(self):
        # Read data from SmartDashboard
        p = wpilib.SmartDashboard.getNumber("P Gain", 0)
        i = wpilib.SmartDashboard.getNumber("I Gain", 0)
        d = wpilib.SmartDashboard.getNumber("D Gain", 0)
        iz = wpilib.SmartDashboard.getNumber("I Zone", 0)
        ff = wpilib.SmartDashboard.getNumber("Feed Forward", 0)
        min_out = wpilib.SmartDashboard.getNumber("Min Output", 0)
        max_out = wpilib.SmartDashboard.getNumber("Max Output", 0)
        rotations = wpilib.SmartDashboard.getNumber("Set Rotations", 0)

        # Update PIDController datapoints with the latest from SmartDashboard
        if(p is not self.coeff['p']):
            self.pidController.setP(p)
            self.coeff['p'] = p
        if(i is not self.coeff['i']):
            self.pidController.setI(pi)
            self.coeff['i'] = i
        if(d is not self.coeff['d']):
            self.pidController.setD(d)
            self.coeff['d'] = d
        if(iz is not self.coeff['iz']):
            self.pidController.setIZone(iz)
            self.coeff['iz'] = iz
        if(ff is not self.coeff['ff']):
            self.pidController.setFF(ff)
            self.coeff['ff'] = ff
        if((min_out is not self.kMinOutput) or
           (max_out is not self.kMaxOutput)):
            self.pidController.setOutputRange(min_out, max_out)
            self.kMinOutput = min_out, self.kMaxOutput = max_out

        # PIDController objects are commanded to a set point using the
        # setReference() method.
        #
        # The first parameter is the value of the set point, whose units vary
        # depending on the control type set in the second parameter.
        #
        # The second parameter is the control type can be set to one of four
        # parameters:
        # rev.ControlType.kDutyCycle
        # rev.ControlType.kPosition
        # rev.ControlType.kVelocity
        # rev.ControlType.kVoltage
        #
        # For more information on what these types are, refer to the Spark Max
        # documentation.
        self.pidController.setReference(rotations, rev.ControlType.kPosition)

        # Push Setpoint and the motor's current position to SmartDashboard.
        wpilib.SmartDashboard.putNumber("Setpoint", rotations)
        wpilib.SmartDashboard.putNumber("Process Variable",
                                        self.encoder.getPosition())


if __name__ == "__main__":
    wpilib.run(Robot)
