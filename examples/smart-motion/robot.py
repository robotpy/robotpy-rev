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
# Graph these values from the Telemetry table in your dashboard, and edit
# coefficients and setpoints in the Tunables table.


class Robot(wpilib.TimedRobot):
    def __init__(self):
        super().__init__()
        # initialize motor
        self.motor = rev.SparkMax(
            wpilib.CANPort.CAN_S0, 1, rev.SparkLowLevel.MotorType.BRUSHLESS
        )

        self.pid_controller = self.motor.get_closed_loop_controller()
        self.encoder = self.motor.get_encoder()

        # PID coefficients
        self.p_gain = 5e-5
        self.i_gain = 1e-6
        self.d_gain = 0
        self.i_zone = 0
        # Convert the legacy duty-cycle/RPM gain to kV in volts/RPM at 12 V.
        self.feed_forward = 0.000156 * 12
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

        # Publish editable PID coefficients in the Tunables table.
        # Use doubles even for integer defaults so fractional tuning is supported.
        self.p_gain_tunable = tunables.add_double("P Gain", self.p_gain)
        self.i_gain_tunable = tunables.add_double("I Gain", self.i_gain)
        self.d_gain_tunable = tunables.add_double("D Gain", self.d_gain)
        self.i_zone_tunable = tunables.add_double("I Zone", self.i_zone)
        self.feed_forward_tunable = tunables.add_double(
            "Feed Forward", self.feed_forward
        )
        self.max_output_tunable = tunables.add_double("Max Output", self.max_output)
        self.min_output_tunable = tunables.add_double("Min Output", self.min_output)

        # Publish editable MAXMotion coefficients and setpoints.
        self.max_velocity_tunable = tunables.add_double("Max Velocity", self.max_vel)
        self.max_acceleration_tunable = tunables.add_double(
            "Max Acceleration", self.max_acc
        )
        self.allowed_error_tunable = tunables.add_double(
            "Allowed Closed Loop Error", self.allowed_err
        )
        self.position_tunable = tunables.add_double("Set Position", 0.0)
        self.velocity_tunable = tunables.add_double("Set Velocity", 0.0)

        # Button to toggle between velocity and MAXMotion modes.
        self.mode_tunable = tunables.add_boolean("Mode", True)

    def _update_closed_loop_config(self):
        self.config.closed_loop.p(self.p_gain)
        self.config.closed_loop.i(self.i_gain)
        self.config.closed_loop.d(self.d_gain)
        self.config.closed_loop.i_zone(self.i_zone)
        self.config.closed_loop.feed_forward.v(self.feed_forward)
        self.config.closed_loop.output_range(self.min_output, self.max_output)

    def _update_max_motion_config(self):
        self.config.closed_loop.max_motion.cruise_velocity(self.max_vel)
        self.config.closed_loop.max_motion.max_acceleration(self.max_acc)
        self.config.closed_loop.allowed_closed_loop_error(self.allowed_err)

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
        max_out = self.max_output_tunable.get()
        min_out = self.min_output_tunable.get()
        max_velocity = self.max_velocity_tunable.get()
        max_acceleration = self.max_acceleration_tunable.get()
        allowed_error = self.allowed_error_tunable.get()

        # If tunable values have changed, write new values to the controller.
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
        if max_out != self.max_output or min_out != self.min_output:
            self.config.closed_loop.output_range(min_out, max_out)
            self.min_output = min_out
            self.max_output = max_out
            self._apply_config()

        if max_velocity != self.max_vel:
            self.config.closed_loop.max_motion.cruise_velocity(max_velocity)
            self.max_vel = max_velocity
            self._apply_config()
        if max_acceleration != self.max_acc:
            self.config.closed_loop.max_motion.max_acceleration(max_acceleration)
            self.max_acc = max_acceleration
            self._apply_config()
        if allowed_error != self.allowed_err:
            self.config.closed_loop.allowed_closed_loop_error(allowed_error)
            self.allowed_err = allowed_error
            self._apply_config()

        mode = self.mode_tunable.get()
        if mode:
            setpoint = self.velocity_tunable.get()
            self.pid_controller.set_setpoint(
                setpoint, rev.SparkBase.ControlType.VELOCITY
            )
            pv = self.encoder.get_velocity().get()
        else:
            setpoint = self.position_tunable.get()
            self.pid_controller.set_setpoint(
                setpoint, rev.SparkBase.ControlType.MAX_MOTION_POSITION_CONTROL
            )
            pv = self.encoder.get_position().get()

        telemetry.log("SetPoint", setpoint)
        telemetry.log("Process Variable", pv)
        telemetry.log("Output", self.motor.get_applied_output().get())


if __name__ == "__main__":
    wpilib.run(Robot)
