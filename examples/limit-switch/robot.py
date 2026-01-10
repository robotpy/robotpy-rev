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


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        # Create motor
        self.motor = rev.SparkMax(1, rev.SparkMax.MotorType.kBrushless)

        self.joystick = wpilib.Joystick(0)

        # A SparkLimitSwitch object is constructed using the
        # getForwardLimitSwitch() or
        # getReverseLimitSwitch() method on an existing CANSparkMax object,
        # depending on which direction you would like to limit
        #
        # Limit switches can be configured to one of two polarities:
        # rev.LimitSwitchConfig.Type.kNormallyOpen
        # rev.LimitSwitchConfig.Type.kNormallyClosed
        self.forwardLimit = self.motor.getForwardLimitSwitch()
        self.reverseLimit = self.motor.getReverseLimitSwitch()

        self.limitConfig = rev.SparkMaxConfig()
        self.limitConfig.limitSwitch.forwardLimitSwitchType(
            rev.LimitSwitchConfig.Type.kNormallyClosed
        ).forwardLimitSwitchEnabled(False).reverseLimitSwitchType(
            rev.LimitSwitchConfig.Type.kNormallyClosed
        ).reverseLimitSwitchEnabled(
            False
        )
        self.motor.configure(
            self.limitConfig,
            rev.ResetMode.kResetSafeParameters,
            rev.PersistMode.kNoPersistParameters,
        )

        self.prevForwardLimitEnabled = (
            self.motor.configAccessor.limitSwitch.getForwardLimitSwitchEnabled()
        )
        self.prevReverseLimitEnabled = (
            self.motor.configAccessor.limitSwitch.getReverseLimitSwitchEnabled()
        )

        wpilib.SmartDashboard.putBoolean(
            "Forward Limit Enabled", self.prevForwardLimitEnabled
        )
        wpilib.SmartDashboard.putBoolean(
            "Reverse Limit Enabled", self.prevReverseLimitEnabled
        )

    def teleopPeriodic(self):
        # Pair motor and the joystick's Y Axis
        self.motor.set(self.joystick.getY())

        # enable/disable limit switches based on value read from SmartDashboard
        if self.prevForwardLimitEnabled != wpilib.SmartDashboard.getBoolean(
            "Forward Limit Enabled", False
        ):
            self.prevForwardLimitEnabled = wpilib.SmartDashboard.getBoolean(
                "Forward Limit Enabled", False
            )
            self.limitConfig.limitSwitch.forwardLimitSwitchEnabled(
                self.prevForwardLimitEnabled
            )
            self.motor.configure(
                self.limitConfig,
                rev.ResetMode.kResetSafeParameters,
                rev.PersistMode.kNoPersistParameters,
            )
        if self.prevReverseLimitEnabled != wpilib.SmartDashboard.getBoolean(
            "Reverse Limit Enabled", False
        ):
            self.prevReverseLimitEnabled = wpilib.SmartDashboard.getBoolean(
                "Reverse Limit Enabled", False
            )
            self.limitConfig.limitSwitch.reverseLimitSwitchEnabled(
                self.prevReverseLimitEnabled
            )
            self.motor.configure(
                self.limitConfig,
                rev.ResetMode.kResetSafeParameters,
                rev.PersistMode.kNoPersistParameters,
            )

        # The get() method can be used on a SparkLimitSwitch object to read the
        # state of the switch.
        #
        # In this example, the polarity of the switches are set to normally
        # closed. In this case, get() will return true if the switch is
        # pressed. It will also return true if you do not have a switch
        # connected. get() will return false when the switch is released.
        wpilib.SmartDashboard.putBoolean(
            "Forward Limit Switch", self.forwardLimit.get()
        )
        wpilib.SmartDashboard.putBoolean(
            "Reverse Limit Switch", self.reverseLimit.get()
        )


if __name__ == "__main__":
    wpilib.run(Robot)
