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

        self.joystick = wpilib.Joystick(0)

        # A SparkLimitSwitch object is constructed using the
        # get_forward_limit_switch() or get_reverse_limit_switch() method on an
        # existing SparkMax object, depending on which direction you would like
        # to limit.
        #
        # Limit switches can be configured to one of two polarities:
        # rev.LimitSwitchConfig.Type.NORMALLY_OPEN
        # rev.LimitSwitchConfig.Type.NORMALLY_CLOSED
        self.forward_limit = self.motor.get_forward_limit_switch()
        self.reverse_limit = self.motor.get_reverse_limit_switch()

        self.limit_config = rev.SparkMaxConfig()
        self.limit_config.limit_switch.forward_limit_switch_type(
            rev.LimitSwitchConfig.Type.NORMALLY_CLOSED
        ).forward_limit_switch_trigger_behavior(
            rev.LimitSwitchConfig.Behavior.STOP_MOVING_MOTOR
        ).reverse_limit_switch_type(
            rev.LimitSwitchConfig.Type.NORMALLY_CLOSED
        ).reverse_limit_switch_trigger_behavior(
            rev.LimitSwitchConfig.Behavior.STOP_MOVING_MOTOR
        )
        self.motor.configure(
            self.limit_config,
            rev.ResetMode.RESET_SAFE_PARAMETERS,
            rev.PersistMode.NO_PERSIST_PARAMETERS,
        )

        self.prev_forward_limit_enabled = (
            self.motor.config_accessor.limit_switch.get_forward_limit_switch_trigger_behavior()
            != 0
        )
        self.prev_reverse_limit_enabled = (
            self.motor.config_accessor.limit_switch.get_reverse_limit_switch_trigger_behavior()
            != 0
        )

        # Publish editable enable flags in the Tunables table.
        self.forward_limit_enabled = tunables.add_boolean(
            "Forward Limit Enabled", self.prev_forward_limit_enabled
        )
        self.reverse_limit_enabled = tunables.add_boolean(
            "Reverse Limit Enabled", self.prev_reverse_limit_enabled
        )

    def teleop_periodic(self):
        # Pair motor output and the joystick's Y Axis
        self.motor.set_voltage(self.joystick.get_y() * 12)

        # Enable/disable limit switches using the latest tunable values.
        if self.prev_forward_limit_enabled != self.forward_limit_enabled.get():
            self.prev_forward_limit_enabled = self.forward_limit_enabled.get()
            self.limit_config.limit_switch.forward_limit_switch_trigger_behavior(
                rev.LimitSwitchConfig.Behavior.STOP_MOVING_MOTOR
                if self.prev_forward_limit_enabled
                else rev.LimitSwitchConfig.Behavior.KEEP_MOVING_MOTOR
            )
            self.motor.configure(
                self.limit_config,
                rev.ResetMode.RESET_SAFE_PARAMETERS,
                rev.PersistMode.NO_PERSIST_PARAMETERS,
            )
        if self.prev_reverse_limit_enabled != self.reverse_limit_enabled.get():
            self.prev_reverse_limit_enabled = self.reverse_limit_enabled.get()
            self.limit_config.limit_switch.reverse_limit_switch_trigger_behavior(
                rev.LimitSwitchConfig.Behavior.STOP_MOVING_MOTOR
                if self.prev_reverse_limit_enabled
                else rev.LimitSwitchConfig.Behavior.KEEP_MOVING_MOTOR
            )
            self.motor.configure(
                self.limit_config,
                rev.ResetMode.RESET_SAFE_PARAMETERS,
                rev.PersistMode.NO_PERSIST_PARAMETERS,
            )

        # The get() method can be used on a SparkLimitSwitch object to read the
        # state of the switch.
        #
        # In this example, the polarity of the switches are set to normally
        # closed. In this case, get() will return true if the switch is
        # pressed. It will also return true if you do not have a switch
        # connected. get() will return false when the switch is released.
        telemetry.log("Forward Limit Switch", self.forward_limit.get().get())
        telemetry.log("Reverse Limit Switch", self.reverse_limit.get().get())


if __name__ == "__main__":
    wpilib.run(Robot)
