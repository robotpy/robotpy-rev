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
        # SPARK MAX controllers are intialized over CAN by constructing a
        # CANSparkMax object
        #
        # The CAN ID, which can be configured using the SPARK MAX Client, is passed
        # as the first parameter
        #
        # The motor type is passed as the second parameter.
        # Motor type can either be:
        #   rev.MotorType.kBrushless
        #   rev.MotorType.kBrushed
        #
        # The example below initializes four brushless motors with CAN IDs
        # 1, 2, 3, 4. Change these parameters to match your setup
        self.leftLeadMotor = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.rightLeadMotor = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.leftFollowMotor = rev.CANSparkMax(2, rev.MotorType.kBrushless)
        self.rightFollowMotor = rev.CANSparkMax(4, rev.MotorType.kBrushless)

        # Passing in the lead motors into DifferentialDrive allows any
        # commmands sent to the lead motors to be sent to the follower motors.
        self.driveTrain = DifferentialDrive(self.leftLeadMotor, self.rightLeadMotor)
        self.joystick = wpilib.Joystick(0)

        # The RestoreFactoryDefaults method can be used to reset the
        # configuration parameters in the SPARK MAX to their factory default
        # state. If no argument is passed, these parameters will not persist
        # between power cycles
        self.leftLeadMotor.restoreFactoryDefaults()
        self.rightLeadMotor.restoreFactoryDefaults()
        self.leftFollowMotor.restoreFactoryDefaults()
        self.rightFollowMotor.restoreFactoryDefaults()

        # In CAN mode, one SPARK MAX can be configured to follow another. This
        # is done by calling the follow() method on the SPARK MAX you want to
        # configure as a follower, and by passing as a parameter the SPARK MAX
        # you want to configure as a leader.
        #
        # This is shown in the example below, where one motor on each side of
        # our drive train is configured to follow a lead motor.
        self.leftFollowMotor.follow(self.leftLeadMotor)
        self.rightFollowMotor.follow(self.rightLeadMotor)

    def teleopPeriodic(self):
        # Drive with arcade style
        self.driveTrain.arcadeDrive(-self.joystick.getY(), self.joystick.getX())


if __name__ == "__main__":
    wpilib.run(Robot)
