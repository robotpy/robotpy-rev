#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# Copyright (c) 2017-2018 FIRST. All Rights Reserved.
# Open Source Software - may be modified and shared by FRC teams. The code
# must be accompanied by the FIRST BSD license file in the root directory of
# the project.
# ----------------------------------------------------------------------------

import rev
import wpilib


# Before Running:
# Open Shuffleboard, select File->Load Layout and select the
# shuffleboard.json that is in the root directory of this example

# REV Smart Motion Guide
#
# The SPARK MAX includes a new control mode, REV Smart Motion which is used to
# control the position of the motor, and includes a max velocity and max
# acceleration parameter to ensure the motor moves in a smooth and predictable
# way. This is done by generating a motion profile on the fly in SPARK MAX and
# controlling the velocity of the motor to follow this profile.
#
# Since REV Smart Motion uses the velocity to track a profile, there are only
# two steps required to configure this mode:
#    1) Tune a velocity PID loop for the mechanism
#    2) Configure the smart motion parameters
#
# Tuning the Velocity PID Loop
#
# The most important part of tuning any closed loop control such as the velocity
# PID, is to graph the inputs and outputs to understand exactly what is happening.
# For tuning the Velocity PID loop, at a minimum we recommend graphing:
#
#    1) The velocity of the mechanism (‘Process variable’)
#    2) The commanded velocity value (‘Setpoint’)
#    3) The applied output
#
# This example will use ShuffleBoard to graph the above parameters. Make sure to
# load the shuffleboard.json file in the root of this directory to get the full
# effect of the GUI layout.


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        # initialize motor
        self.motor = rev.CANSparkMax(1, rev.MotorType.kBrushless)

        # The RestoreFactoryDefaults method can be used to reset the configuration parameters
        # in the SPARK MAX to their factory default state. If no argument is passed, these
        # parameters will not persist between power cycles
        self.motor.restoreFactoryDefaults()

        self.pid_controller = self.motor.getPIDController()
        self.encoder = self.motor.getEncoder()

        # PID coefficients
        self.kP = 5e-5
        self.kI = 1e-6
        self.kD = 0
        self.kIz = 0
        self.kFF = 0.000156
        self.kMaxOutput = 1
        self.kMinOutput = -1
        self.max_rpm = 5700

        # Smart Motion coefficients
        self.max_vel = 1500  # rpm
        self.max_acc = 500
        self.min_vel = 0
        self.allowed_err = 0

        # set PID coefficients
        self.pid_controller.setP(self.kP)
        self.pid_controller.setI(self.kI)
        self.pid_controller.setD(self.kD)
        self.pid_controller.setIZone(self.kIz)
        self.pid_controller.setFF(self.kFF)
        self.pid_controller.setOutputRange(self.kMinOutput, self.kMaxOutput)

        # Smart Motion coefficients are set on a CANPIDController object
        #
        # - setSmartMotionMaxVelocity() will limit the velocity in RPM of
        # the pid controller in Smart Motion mode
        # - setSmartMotionMinOutputVelocity() will put a lower bound in
        # RPM of the pid controller in Smart Motion mode
        # - setSmartMotionMaxAccel() will limit the acceleration in RPM^2
        # of the pid controller in Smart Motion mode
        # - setSmartMotionAllowedClosedLoopError() will set the max allowed
        # error for the pid controller in Smart Motion mode
        smart_motion_slot = 0
        self.pid_controller.setSmartMotionMaxVelocity(self.max_vel, smart_motion_slot)
        self.pid_controller.setSmartMotionMinOutputVelocity(
            self.min_vel, smart_motion_slot
        )
        self.pid_controller.setSmartMotionMaxAccel(self.max_acc, smart_motion_slot)
        self.pid_controller.setSmartMotionAllowedClosedLoopError(
            self.allowed_err, smart_motion_slot
        )

        # display PID coefficients on SmartDashboard
        wpilib.SmartDashboard.putNumber("P Gain", self.kP)
        wpilib.SmartDashboard.putNumber("I Gain", self.kI)
        wpilib.SmartDashboard.putNumber("D Gain", self.kD)
        wpilib.SmartDashboard.putNumber("I Zone", self.kIz)
        wpilib.SmartDashboard.putNumber("Feed Forward", self.kFF)
        wpilib.SmartDashboard.putNumber("Max Output", self.kMaxOutput)
        wpilib.SmartDashboard.putNumber("Min Output", self.kMinOutput)

        # display Smart Motion coefficients
        wpilib.SmartDashboard.putNumber("Max Velocity", self.max_vel)
        wpilib.SmartDashboard.putNumber("Min Velocity", self.min_vel)
        wpilib.SmartDashboard.putNumber("Max Acceleration", self.max_acc)
        wpilib.SmartDashboard.putNumber("Allowed Closed Loop Error", self.allowed_err)
        wpilib.SmartDashboard.putNumber("Set Position", 0)
        wpilib.SmartDashboard.putNumber("Set Velocity", 0)

        # button to toggle between velocity and smart motion modes
        wpilib.SmartDashboard.putBoolean("Mode", True)

    def teleopPeriodic(self):
        # read PID coefficients from SmartDashboard
        p = wpilib.SmartDashboard.getNumber("P Gain", 0)
        i = wpilib.SmartDashboard.getNumber("I Gain", 0)
        d = wpilib.SmartDashboard.getNumber("D Gain", 0)
        iz = wpilib.SmartDashboard.getNumber("I Zone", 0)
        ff = wpilib.SmartDashboard.getNumber("Feed Forward", 0)
        max_out = wpilib.SmartDashboard.getNumber("Max Output", 0)
        min_out = wpilib.SmartDashboard.getNumber("Min Output", 0)
        maxV = wpilib.SmartDashboard.getNumber("Max Velocity", 0)
        minV = wpilib.SmartDashboard.getNumber("Min Velocity", 0)
        maxA = wpilib.SmartDashboard.getNumber("Max Acceleration", 0)
        allE = wpilib.SmartDashboard.getNumber("Allowed Closed Loop Error", 0)

        # if PID coefficients on SmartDashboard have changed, write new values to controller
        if p != self.kP:
            self.pid_controller.setP(p)
            self.kP = p
        if i != self.kI:
            self.pid_controller.setI(i)
            self.kI = i
        if d != self.kD:
            self.pid_controller.setD(d)
            self.kD = d
        if iz != self.kIz:
            self.pid_controller.setIZone(iz)
            self.kIz = iz
        if ff != self.kFF:
            self.pid_controller.setFF(ff)
            self.kFF = ff
        if max_out != self.kMaxOutput or min_out != self.kMinOutput:
            self.pid_controller.setOutputRange(min_out, max_out)
            self.kMinOutput = min_out
            self.kMaxOutput = max_out

        if maxV != self.max_vel:
            self.pid_controller.setSmartMotionMaxVelocity(maxV, 0)
            self.max_vel = maxV
        if minV != self.min_vel:
            self.pid_controller.setSmartMotionMinOutputVelocity(minV, 0)
            self.min_vel = minV
        if maxA != self.max_acc:
            self.pid_controller.setSmartMotionMaxAccel(maxA, 0)
            self.max_acc = maxA
        if allE != self.allowed_err:
            self.pid_controller.setSmartMotionAllowedClosedLoopError(allE, 0)
            self.allowed_err = allE

        mode = wpilib.SmartDashboard.getBoolean("Mode", False)
        if mode:
            setpoint = wpilib.SmartDashboard.getNumber("Set Velocity", 0)
            self.pid_controller.setReference(setpoint, rev.ControlType.kVelocity)
            pv = self.encoder.getVelocity()
        else:
            setpoint = wpilib.SmartDashboard.getNumber("Set Position", 0)
            # As with other PID modes, Smart Motion is set by calling the
            # setReference method on an existing pid object and setting
            # the control type to kSmartMotion
            self.pid_controller.setReference(setpoint, rev.ControlType.kSmartMotion)
            pv = self.encoder.getPosition()

        wpilib.SmartDashboard.putNumber("SetPoint", setpoint)
        wpilib.SmartDashboard.putNumber("Process Variable", pv)
        wpilib.SmartDashboard.putNumber("Output", self.motor.getAppliedOutput())


if __name__ == "__main__":
    wpilib.run(Robot)
