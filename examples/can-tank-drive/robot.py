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
        # The example below initializes two brushless motors with CAN IDs
        # 1 and 2. Change these parameters to match your setup
        self.leftMotor = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.rightMotor = rev.CANSparkMax(2, rev.MotorType.kBrushless)

        # The RestoreFactoryDefaults method can be used to reset the
        # configuration parameters in the SPARK MAX to their factory default
        # state. If no argument is passed, these parameters will not persist
        # between power cycles
        self.leftMotor.restoreFactoryDefaults()
        self.rightMotor.restoreFactoryDefaults()

        self.driveTrain = DifferentialDrive(self.leftMotor, self.rightMotor)
        self.l_stick = wpilib.Joystick(0)
        self.r_stick = wpilib.Joystick(1)

    def teleopPeriodic(self):
        # Create tank drive
        self.driveTrain.tankDrive(self.l_stick.getY(), self.r_stick.getY())


if __name__ == "__main__":
    wpilib.run(Robot)
