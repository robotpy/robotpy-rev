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


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        # Create motor
        self.motor = rev.CANSparkMax(1, rev.MotorType.kBrushless)

        self.joystick = wpilib.Joystick(0)

        # A CANDigitalInput object is constructed using the
        # GetForwardLimitSwitch() or
        # GetReverseLimitSwitch() method on an existing CANSparkMax object,
        # depending on which direction you would like to limit
        #
        # Limit switches can be configured to one of two polarities:
        # rev.CANDigitalInput.LimitSwitchPolarity.kNormallyOpen
        # rev.CANDigitalInput.LimitSwitchPolarity.kNormallyClosed
        self.forwardLimit = self.motor.getForwardLimitSwitch(
            rev.LimitSwitchPolarity.kNormallyClosed
        )
        self.reverseLimit = self.motor.getReverseLimitSwitch(
            rev.LimitSwitchPolarity.kNormallyClosed
        )

        self.forwardLimit.enableLimitSwitch(False)
        self.reverseLimit.enableLimitSwitch(False)

        wpilib.SmartDashboard.putBoolean(
            "Forward Limit Enabled", self.forwardLimit.isLimitSwitchEnabled()
        )
        wpilib.SmartDashboard.putBoolean(
            "Reverse Limit Enabled", self.forwardLimit.isLimitSwitchEnabled()
        )

    def teleopPeriodic(self):
        # Pair motor and the joystick's Y Axis
        self.motor.set(self.joystick.getY())

        # enable/disable limit switches based on value read from SmartDashboard
        self.forwardLimit.enableLimitSwitch(
            wpilib.SmartDashboard.getBoolean("Forward Limit Enabled", False)
        )
        self.reverseLimit.enableLimitSwitch(
            wpilib.SmartDashboard.getBoolean("Reverse Limit Enabled", False)
        )

        # The get() method can be used on a CANDigitalInput object to read the
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
