#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import wpilib

from robotcontainer import RobotContainer


class Robot(wpilib.TimedRobot):
    """
    The robot is configured to automatically run this class, and to call the
    methods corresponding to each mode, as described in the TimedRobot
    documentation.
    """

    def __init__(self) -> None:
        """
        This function is run when the robot is first started up and should be used
        for any initialization code.
        """
        super().__init__()
        self.autonomous_command = None

        # Instantiate our RobotContainer.  This will perform all our button bindings,
        # and put our autonomous chooser on the dashboard.
        self.robot_container = RobotContainer()

    def robot_periodic(self) -> None:
        """
        This function is called every 20 ms, no matter the mode. Use this for items
        like diagnostics that you want ran during disabled, autonomous, teleoperated
        and utility.
        """
        # Runs the Scheduler.  This is responsible for polling buttons, adding
        # newly-scheduled commands, running already-scheduled commands, removing
        # finished or interrupted commands, and running subsystem periodic() methods.
        # This must be called from the robot's periodic block in order for anything
        # in the Command-based framework to work.
        commands2.CommandScheduler.get_instance().run()

    def disabled_init(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""

    def disabled_periodic(self) -> None:
        pass

    def autonomous_init(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        self.autonomous_command = self.robot_container.get_autonomous_command()

        # schedule the autonomous command (example)
        if self.autonomous_command is not None:
            commands2.CommandScheduler.get_instance().schedule(self.autonomous_command)

    def autonomous_periodic(self) -> None:
        """This function is called periodically during autonomous."""

    def teleop_init(self) -> None:
        # This makes sure that the autonomous stops running when
        # teleop starts running. If you want the autonomous to
        # continue until interrupted by another command, remove
        # this line or comment it out.
        if self.autonomous_command is not None:
            self.autonomous_command.cancel()

    def teleop_periodic(self) -> None:
        """This function is called periodically during operator control."""

    def utility_init(self) -> None:
        # Cancels all running commands at the start of utility (formerly test) mode.
        commands2.CommandScheduler.get_instance().cancel_all()

    def utility_periodic(self) -> None:
        """This function is called periodically during utility mode."""


if __name__ == "__main__":
    wpilib.run(Robot)
