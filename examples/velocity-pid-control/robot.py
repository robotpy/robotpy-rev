#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import rev
import telemetry
import tunables
import wpilib


class Robot(wpilib.TimedRobot):
    def __init__(self):
        super().__init__()
        # Create motor
        self.motor = rev.SparkMax(
            wpilib.CANPort.CAN_S0, 1, rev.SparkLowLevel.MotorType.BRUSHLESS
        )

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
        self.feed_forward = 0  # kV in volts/RPM
        self.min_output = -1
        self.max_output = 1

        # Motor max RPM
        self.max_rpm = 5700

        self.config = rev.SparkMaxConfig()
        self._update_closed_loop_config()
        self._apply_config()

        # Publish editable PID coefficients in the Tunables table.
        # Use doubles even for integer defaults so fractional tuning is supported.
        self.p_gain_tunable = tunables.add_double("P Gain", self.p_gain)
        self.i_gain_tunable = tunables.add_double("I Gain", self.i_gain)
        self.d_gain_tunable = tunables.add_double("D Gain", self.d_gain)
        self.i_zone_tunable = tunables.add_double("I Zone", self.i_zone)
        self.feed_forward_tunable = tunables.add_double(
            "Feed Forward", self.feed_forward
        )
        self.min_output_tunable = tunables.add_double("Min Output", self.min_output)
        self.max_output_tunable = tunables.add_double("Max Output", self.max_output)

    def _update_closed_loop_config(self):
        self.config.closed_loop.p(self.p_gain)
        self.config.closed_loop.i(self.i_gain)
        self.config.closed_loop.d(self.d_gain)
        self.config.closed_loop.i_zone(self.i_zone)
        self.config.closed_loop.feed_forward.v(self.feed_forward)
        self.config.closed_loop.output_range(self.min_output, self.max_output)

    def _apply_config(self):
        self.motor.configure(
            self.config,
            rev.ResetMode.RESET_SAFE_PARAMETERS,
            rev.PersistMode.NO_PERSIST_PARAMETERS,
        )

    def teleop_periodic(self):
        # Read the latest dashboard values from the tunables.
        p = self.p_gain_tunable.get()
        i = self.i_gain_tunable.get()
        d = self.d_gain_tunable.get()
        iz = self.i_zone_tunable.get()
        ff = self.feed_forward_tunable.get()
        min_out = self.min_output_tunable.get()
        max_out = self.max_output_tunable.get()

        # Update closed loop config with the latest tunable values.
        if p != self.p_gain:
            self.config.closed_loop.p(p)
            self.p_gain = p
            self._apply_config()
        if i != self.i_gain:
            self.config.closed_loop.i(i)
            self.i_gain = i
            self._apply_config()
        if d != self.d_gain:
            self.config.closed_loop.d(d)
            self.d_gain = d
            self._apply_config()
        if iz != self.i_zone:
            self.config.closed_loop.i_zone(iz)
            self.i_zone = iz
            self._apply_config()
        if ff != self.feed_forward:
            self.config.closed_loop.feed_forward.v(ff)
            self.feed_forward = ff
            self._apply_config()
        if (min_out != self.min_output) or (max_out != self.max_output):
            self.config.closed_loop.output_range(min_out, max_out)
            self.min_output = min_out
            self.max_output = max_out
            self._apply_config()

        setpoint = self.max_rpm * self.joystick.get_y()

        # Closed loop controllers are commanded to a set point using the
        # set_setpoint() method.
        #
        # The first parameter is the value of the set point, whose units vary
        # depending on the control type set in the second parameter.
        self.pid_controller.set_setpoint(setpoint, rev.SparkBase.ControlType.VELOCITY)

        # Log the setpoint and the motor's current velocity to the Telemetry table.
        telemetry.log("SetPoint", setpoint)
        telemetry.log("ProcessVariable", self.encoder.get_velocity().get())


if __name__ == "__main__":
    wpilib.run(Robot)
