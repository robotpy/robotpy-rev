#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import wpilib

from robotcontainer import RobotContainer


class MyRobot(commands2.TimedCommandRobot):
    def robot_init(self):
        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        self.container = RobotContainer()
        self.autonomous_command = None

    def autonomous_init(self) -> None:
        self.autonomous_command = self.container.get_autonomous_command()

        if self.autonomous_command:
            self.autonomous_command.schedule()

    def teleop_init(self) -> None:
        if self.autonomous_command:
            self.autonomous_command.cancel()

    def test_init(self) -> None:
        commands2.CommandScheduler.get_instance().cancel_all()


if __name__ == "__main__":
    wpilib.run(MyRobot)
