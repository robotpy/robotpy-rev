#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import rev
import wpilib

# Before Running:
# Open Shuffleboard, select File->Load Layout and select the
# shuffleboard.json that is in the root directory of this example

# REV MAXMotion Guide
#
# The SPARK MAX includes a profiled closed-loop control mode, MAXMotion, which
# is used to control the position of the motor and includes max velocity and max
# acceleration parameters to ensure the motor moves in a smooth and predictable
# way. This is done by generating a motion profile on the fly in SPARK MAX and
# controlling the velocity of the motor to follow this profile.
#
# Since MAXMotion uses the velocity to track a profile, there are only two steps
# required to configure this mode:
#    1) Tune a velocity PID loop for the mechanism
#    2) Configure the MAXMotion parameters
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
    def robot_init(self):
        # initialize motor
        self.motor = rev.SparkMax(0, 1, rev.SparkLowLevel.MotorType.BRUSHLESS)

        self.pid_controller = self.motor.get_closed_loop_controller()
        self.encoder = self.motor.get_encoder()

        # PID coefficients
        self.p_gain = 5e-5
        self.i_gain = 1e-6
        self.d_gain = 0
        self.i_zone = 0
        self.feed_forward = 0.000156
        self.max_output = 1
        self.min_output = -1
        self.max_rpm = 5700

        # MAXMotion coefficients
        self.max_vel = 1500  # rpm
        self.max_acc = 500
        self.allowed_err = 0

        self.config = rev.SparkMaxConfig()
        self._update_closed_loop_config()
        self._update_max_motion_config()
        self._apply_config()

        # display PID coefficients on SmartDashboard
        wpilib.SmartDashboard.put_number("P Gain", self.p_gain)
        wpilib.SmartDashboard.put_number("I Gain", self.i_gain)
        wpilib.SmartDashboard.put_number("D Gain", self.d_gain)
        wpilib.SmartDashboard.put_number("I Zone", self.i_zone)
        wpilib.SmartDashboard.put_number("Feed Forward", self.feed_forward)
        wpilib.SmartDashboard.put_number("Max Output", self.max_output)
        wpilib.SmartDashboard.put_number("Min Output", self.min_output)

        # display MAXMotion coefficients
        wpilib.SmartDashboard.put_number("Max Velocity", self.max_vel)
        wpilib.SmartDashboard.put_number("Max Acceleration", self.max_acc)
        wpilib.SmartDashboard.put_number("Allowed Closed Loop Error", self.allowed_err)
        wpilib.SmartDashboard.put_number("Set Position", 0)
        wpilib.SmartDashboard.put_number("Set Velocity", 0)

        # button to toggle between velocity and MAXMotion modes
        wpilib.SmartDashboard.put_boolean("Mode", True)

    def _update_closed_loop_config(self):
        self.config.closed_loop.P(self.p_gain)
        self.config.closed_loop.I(self.i_gain)
        self.config.closed_loop.D(self.d_gain)
        self.config.closed_loop.i_zone(self.i_zone)
        self.config.closed_loop.velocity_ff(self.feed_forward)
        self.config.closed_loop.output_range(self.min_output, self.max_output)

    def _update_max_motion_config(self):
        self.config.closed_loop.max_motion.max_velocity(self.max_vel)
        self.config.closed_loop.max_motion.max_acceleration(self.max_acc)
        self.config.closed_loop.max_motion.allowed_closed_loop_error(self.allowed_err)

    def _apply_config(self):
        self.motor.configure(
            self.config,
            rev.ResetMode.RESET_SAFE_PARAMETERS,
            rev.PersistMode.NO_PERSIST_PARAMETERS,
        )

    def teleop_periodic(self):
        # read PID coefficients from SmartDashboard
        p = wpilib.SmartDashboard.get_number("P Gain", 0)
        i = wpilib.SmartDashboard.get_number("I Gain", 0)
        d = wpilib.SmartDashboard.get_number("D Gain", 0)
        iz = wpilib.SmartDashboard.get_number("I Zone", 0)
        ff = wpilib.SmartDashboard.get_number("Feed Forward", 0)
        max_out = wpilib.SmartDashboard.get_number("Max Output", 0)
        min_out = wpilib.SmartDashboard.get_number("Min Output", 0)
        max_velocity = wpilib.SmartDashboard.get_number("Max Velocity", 0)
        max_acceleration = wpilib.SmartDashboard.get_number("Max Acceleration", 0)
        allowed_error = wpilib.SmartDashboard.get_number("Allowed Closed Loop Error", 0)

        # if config values on SmartDashboard have changed, write new values to controller
        if p != self.p_gain:
            self.config.closed_loop.P(p)
            self.p_gain = p
            self._apply_config()
        if i != self.i_gain:
            self.config.closed_loop.I(i)
            self.i_gain = i
            self._apply_config()
        if d != self.d_gain:
            self.config.closed_loop.D(d)
            self.d_gain = d
            self._apply_config()
        if iz != self.i_zone:
            self.config.closed_loop.i_zone(iz)
            self.i_zone = iz
            self._apply_config()
        if ff != self.feed_forward:
            self.config.closed_loop.velocity_ff(ff)
            self.feed_forward = ff
            self._apply_config()
        if max_out != self.max_output or min_out != self.min_output:
            self.config.closed_loop.output_range(min_out, max_out)
            self.min_output = min_out
            self.max_output = max_out
            self._apply_config()

        if max_velocity != self.max_vel:
            self.config.closed_loop.max_motion.max_velocity(max_velocity)
            self.max_vel = max_velocity
            self._apply_config()
        if max_acceleration != self.max_acc:
            self.config.closed_loop.max_motion.max_acceleration(max_acceleration)
            self.max_acc = max_acceleration
            self._apply_config()
        if allowed_error != self.allowed_err:
            self.config.closed_loop.max_motion.allowed_closed_loop_error(allowed_error)
            self.allowed_err = allowed_error
            self._apply_config()

        mode = wpilib.SmartDashboard.get_boolean("Mode", False)
        if mode:
            setpoint = wpilib.SmartDashboard.get_number("Set Velocity", 0)
            self.pid_controller.set_reference(
                setpoint, rev.SparkBase.ControlType.VELOCITY
            )
            pv = self.encoder.get_velocity()
        else:
            setpoint = wpilib.SmartDashboard.get_number("Set Position", 0)
            self.pid_controller.set_reference(
                setpoint, rev.SparkBase.ControlType.MAX_MOTION_POSITION_CONTROL
            )
            pv = self.encoder.get_position()

        wpilib.SmartDashboard.put_number("SetPoint", setpoint)
        wpilib.SmartDashboard.put_number("Process Variable", pv)
        wpilib.SmartDashboard.put_number("Output", self.motor.get_applied_output())


if __name__ == "__main__":
    wpilib.run(Robot)
