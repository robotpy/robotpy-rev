#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import rev
import wpilib


class Robot(wpilib.TimedRobot):
    def robot_init(self):
        # Create motor
        self.motor = rev.SparkMax(0, 1, rev.SparkLowLevel.MotorType.BRUSHLESS)

        # Use the SPARK closed loop controller for PID functionality.
        self.pid_controller = self.motor.get_closed_loop_controller()

        # Instantiate built-in encoder to display velocity
        self.encoder = self.motor.get_encoder()

        self.joystick = wpilib.Joystick(0)

        # PID Coefficents and Controller Output Range
        self.p_gain = 0.1
        self.i_gain = 1e-4
        self.d_gain = 0
        self.i_zone = 0
        self.feed_forward = 0
        self.min_output = -1
        self.max_output = 1

        # Motor max RPM
        self.max_rpm = 5700

        self.config = rev.SparkMaxConfig()
        self._update_closed_loop_config()
        self._apply_config()

        # Push PID Coefficients to SmartDashboard
        wpilib.SmartDashboard.put_number("P Gain", self.p_gain)
        wpilib.SmartDashboard.put_number("I Gain", self.i_gain)
        wpilib.SmartDashboard.put_number("D Gain", self.d_gain)
        wpilib.SmartDashboard.put_number("I Zone", self.i_zone)
        wpilib.SmartDashboard.put_number("Feed Forward", self.feed_forward)
        wpilib.SmartDashboard.put_number("Min Output", self.min_output)
        wpilib.SmartDashboard.put_number("Max Output", self.max_output)

    def _update_closed_loop_config(self):
        self.config.closed_loop.P(self.p_gain)
        self.config.closed_loop.I(self.i_gain)
        self.config.closed_loop.D(self.d_gain)
        self.config.closed_loop.i_zone(self.i_zone)
        self.config.closed_loop.velocity_ff(self.feed_forward)
        self.config.closed_loop.output_range(self.min_output, self.max_output)

    def _apply_config(self):
        self.motor.configure(
            self.config,
            rev.ResetMode.RESET_SAFE_PARAMETERS,
            rev.PersistMode.NO_PERSIST_PARAMETERS,
        )

    def teleop_periodic(self):
        # Read data from SmartDashboard
        p = wpilib.SmartDashboard.get_number("P Gain", 0)
        i = wpilib.SmartDashboard.get_number("I Gain", 0)
        d = wpilib.SmartDashboard.get_number("D Gain", 0)
        iz = wpilib.SmartDashboard.get_number("I Zone", 0)
        ff = wpilib.SmartDashboard.get_number("Feed Forward", 0)
        min_out = wpilib.SmartDashboard.get_number("Min Output", 0)
        max_out = wpilib.SmartDashboard.get_number("Max Output", 0)

        # Update closed loop config with the latest values from SmartDashboard.
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
        if (min_out != self.min_output) or (max_out != self.max_output):
            self.config.closed_loop.output_range(min_out, max_out)
            self.min_output = min_out
            self.max_output = max_out
            self._apply_config()

        setpoint = self.max_rpm * self.joystick.get_y()

        # Closed loop controllers are commanded to a set point using the
        # set_reference() method.
        #
        # The first parameter is the value of the set point, whose units vary
        # depending on the control type set in the second parameter.
        self.pid_controller.set_reference(setpoint, rev.SparkBase.ControlType.VELOCITY)

        # Push Setpoint and the motor's current velocity to SmartDashboard.
        wpilib.SmartDashboard.put_number("SetPoint", setpoint)
        wpilib.SmartDashboard.put_number("ProcessVariable", self.encoder.get_velocity())


if __name__ == "__main__":
    wpilib.run(Robot)
