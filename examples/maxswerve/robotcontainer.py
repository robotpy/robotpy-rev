#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import math

import commands2
import commands2.button
import wpilib
import wpimath
from wpimath import (
    DrivetrainSplineTrajectoryGenerator,
    PIDController,
    Pose2d,
    ProfiledPIDControllerRadians,
    Rotation2d,
    TrajectoryConfig,
    Translation2d,
)

from constants import AutoConstants, DriveConstants, OIConstants
from subsystems.drivesubsystem import DriveSubsystem
from swervecontrollercommand import SwerveControllerCommand


class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        """The container for the robot. Contains subsystems, OI devices, and commands."""
        # The robot's subsystems
        self.robot_drive = DriveSubsystem()

        # The driver's controller
        self.driver_controller = wpilib.XboxController(
            OIConstants.DRIVER_CONTROLLER_PORT
        )

        # Configure the button bindings
        self.configure_button_bindings()

        # Configure default commands
        self.robot_drive.set_default_command(
            # The left stick controls translation of the robot.
            # Turning is controlled by the X axis of the right stick.
            commands2.RunCommand(
                lambda: self.robot_drive.drive(
                    -wpimath.apply_deadband(
                        self.driver_controller.get_left_y(), OIConstants.DRIVE_DEADBAND
                    ),
                    -wpimath.apply_deadband(
                        self.driver_controller.get_left_x(), OIConstants.DRIVE_DEADBAND
                    ),
                    -wpimath.apply_deadband(
                        self.driver_controller.get_right_x(), OIConstants.DRIVE_DEADBAND
                    ),
                    True,
                ),
                self.robot_drive,
            )
        )

    def configure_button_bindings(self) -> None:
        """
        Use this method to define your button->command mappings. Buttons can be
        created by instantiating a :class:`wpilib.GenericHID` or one of its
        subclasses (:class:`wpilib.Joystick` or :class:`wpilib.XboxController`),
        and then passing it to a :class:`commands2.button.JoystickButton`.
        """
        driver_hid = self.driver_controller.get_hid()

        commands2.button.JoystickButton(
            driver_hid, wpilib.XboxController.Button.RIGHT_BUMPER.value
        ).while_true(commands2.RunCommand(self.robot_drive.set_x, self.robot_drive))

        commands2.button.JoystickButton(
            driver_hid, wpilib.XboxController.Button.MENU.value
        ).on_true(
            commands2.InstantCommand(self.robot_drive.zero_heading, self.robot_drive)
        )

    def get_autonomous_command(self) -> commands2.Command:
        """Use this to pass the autonomous command to the main :class:`.Robot` class.

        :returns: the command to run in autonomous
        """
        # Create config for trajectory
        config = TrajectoryConfig(
            AutoConstants.MAX_SPEED_METERS_PER_SECOND,
            AutoConstants.MAX_ACCELERATION_METERS_PER_SECOND_SQUARED,
        )
        # Add kinematics to ensure max speed is actually obeyed
        config.set_kinematics(DriveConstants.DRIVE_KINEMATICS)

        # An example trajectory to follow. All units in meters.
        example_trajectory = DrivetrainSplineTrajectoryGenerator.generate(
            # Start at the origin facing the +X direction
            Pose2d(0, 0, Rotation2d(0)),
            # Pass through these two interior waypoints, making an 's' curve path
            [Translation2d(1, 1), Translation2d(2, -1)],
            # End 3 meters straight ahead of where we started, facing forward
            Pose2d(3, 0, Rotation2d(0)),
            config,
        )

        theta_controller = ProfiledPIDControllerRadians(
            AutoConstants.P_THETA_CONTROLLER,
            0,
            0,
            AutoConstants.THETA_CONTROLLER_CONSTRAINTS,
        )
        theta_controller.enable_continuous_input(-math.pi, math.pi)

        swerve_controller_command = SwerveControllerCommand(
            example_trajectory,
            self.robot_drive.get_pose,  # Functional interface to feed supplier
            DriveConstants.DRIVE_KINEMATICS,
            # Position controllers
            PIDController(AutoConstants.P_X_CONTROLLER, 0, 0),
            PIDController(AutoConstants.P_Y_CONTROLLER, 0, 0),
            theta_controller,
            self.robot_drive.set_module_states,
            self.robot_drive,
        )

        # Reset odometry to the starting pose of the trajectory.
        self.robot_drive.reset_odometry(example_trajectory.initial_pose())

        # Run path following command, then stop at the end.
        return swerve_controller_command.and_then(
            commands2.InstantCommand(lambda: self.robot_drive.drive(0, 0, 0, False))
        )
