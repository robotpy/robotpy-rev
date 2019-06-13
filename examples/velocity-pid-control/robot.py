# ----------------------------------------------------------------------------
# Copyright (c) 2017-2018 FIRST. All Rights Reserved.
# Open Source Software - may be modified and shared by FRC teams. The code
# must be accompanied by the FIRST BSD license file in the root directory of
# the project.
# ----------------------------------------------------------------------------

import rev
import wpilib


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        # Create motors
        self.motor = rev.CANSparkMax(1, rev.MotorType.kBrushless)

        # You must call getPIDController() on an existing CANSparkMax or
        # SparkMax object to fully use PID functionality
        self.pidController = self.motor.getPIDController()

        # Instantiate built-in encoder to display position
        self.encoder = self.motor.getEncoder()

        self.joystick = wpilib.Joystick(0)

        # PID Coefficents and Controller Output Range
        self.kP = 0.1
        self.kI = 1e-4
        self.kD = 0
        self.kIz = 0
        self.kFF = 0
        self.kMinOutput = -1
        self.kMaxOutput = 1

        # Motor max RPM
        self.maxRPM = 5700

        # The restoreFactoryDefaults() method can be used to reset the
        # configuration parameters in the SPARK MAX to their factory default
        # state. If no argument is passed, these parameters will not persist
        # between power cycles
        self.motor.restoreFactoryDefaults()

        # Set PID Constants
        self.pidController.setP(self.kP)
        self.pidController.setI(self.kI)
        self.pidController.setD(self.kD)
        self.pidController.setIZone(self.kIz)
        self.pidController.setFF(self.kFF)
        self.pidController.setOutputRange(self.kMinOutput, self.kMaxOutput)

        # Push PID Coefficients to SmartDashboard
        wpilib.SmartDashboard.putNumber("P Gain", self.kP)
        wpilib.SmartDashboard.putNumber("I Gain", self.kI)
        wpilib.SmartDashboard.putNumber("D Gain", self.kD)
        wpilib.SmartDashboard.putNumber("I Zone", self.kIz)
        wpilib.SmartDashboard.putNumber("Feed Forward", self.kFF)
        wpilib.SmartDashboard.putNumber("Min Output", self.kMinOutput)
        wpilib.SmartDashboard.putNumber("Max Output", self.kMaxOutput)

    def teleopPeriodic(self):
        # Read data from SmartDashboard
        p = wpilib.SmartDashboard.getNumber("P Gain", 0)
        i = wpilib.SmartDashboard.getNumber("I Gain", 0)
        d = wpilib.SmartDashboard.getNumber("D Gain", 0)
        iz = wpilib.SmartDashboard.getNumber("I Zone", 0)
        ff = wpilib.SmartDashboard.getNumber("Feed Forward", 0)
        min_out = wpilib.SmartDashboard.getNumber("Min Output", 0)
        max_out = wpilib.SmartDashboard.getNumber("Max Output", 0)

        # Update PIDController datapoints with the latest from SmartDashboard
        if p != self.kP:
            self.pidController.setP(p)
            self.kP = p
        if i != self.kI:
            self.pidController.setI(i)
            self.kI = i
        if d != self.kD:
            self.pidController.setD(d)
            self.kD = d
        if iz != self.kIz:
            self.pidController.setIZone(iz)
            self.kIz = iz
        if ff != self.kFF:
            self.pidController.setFF(ff)
            self.kFF = ff
        if (min_out != self.kMinOutput) or (max_out != self.kMaxOutput):
            self.pidController.setOutputRange(min_out, max_out)
            self.kMinOutput = min_out
            self.kMaxOutput = max_out

        setpoint = self.maxRPM * self.joystick.getY()

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
        self.pidController.setReference(setpoint, rev.ControlType.kVelocity)

        # Push Setpoint and the motor's current velocity to SmartDashboard.
        wpilib.SmartDashboard.putNumber("SetPoint", setpoint)
        wpilib.SmartDashboard.putNumber("ProcessVariable", self.encoder.getVelocity())


if __name__ == "__main__":
    wpilib.run(Robot)
