#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import typing

import commands2
import wpilib
from wpimath import (
    ChassisVelocities,
    DrivetrainSplineTrajectory,
    PIDController,
    Pose2d,
    ProfiledPIDControllerRadians,
    SwerveDrive4Kinematics,
    SwerveModuleVelocity,
)


class SwerveControllerCommand(commands2.Command):
    """A command that uses two PID controllers (x and y) and a profiled PID
    controller (theta) to follow a trajectory with a swerve drive.

    The x and y controllers correct the robot's field-relative position, adding
    to the trajectory's field-relative velocity. The theta controller turns the
    robot to the heading of the trajectory's final pose.

    WPILib 2027 no longer provides SwerveControllerCommand or
    HolonomicDriveController, so this is a minimal version of the pair that
    REV's MAXSwerve template uses for its autonomous routine.
    """

    def __init__(
        self,
        trajectory: DrivetrainSplineTrajectory,
        pose: typing.Callable[[], Pose2d],
        kinematics: SwerveDrive4Kinematics,
        x_controller: PIDController,
        y_controller: PIDController,
        theta_controller: ProfiledPIDControllerRadians,
        output_module_states: typing.Callable[
            [
                tuple[
                    SwerveModuleVelocity,
                    SwerveModuleVelocity,
                    SwerveModuleVelocity,
                    SwerveModuleVelocity,
                ]
            ],
            None,
        ],
        *requirements: commands2.Subsystem,
    ) -> None:
        super().__init__()
        self.trajectory = trajectory
        self.pose = pose
        self.kinematics = kinematics
        self.x_controller = x_controller
        self.y_controller = y_controller
        self.theta_controller = theta_controller
        self.output_module_states = output_module_states
        self.desired_rotation = trajectory.end().pose.rotation()
        self.timer = wpilib.Timer()
        self.add_requirements(*requirements)

    def initialize(self) -> None:
        self.timer.restart()
        self.theta_controller.reset(self.pose().rotation().radians())

    def execute(self) -> None:
        desired_state = self.trajectory.sample_at(self.timer.get())
        current_pose = self.pose()

        # The trajectory's velocity is field-relative, like the corrections.
        x_speed = desired_state.velocity.vx + self.x_controller.calculate(
            current_pose.x, desired_state.pose.x
        )
        y_speed = desired_state.velocity.vy + self.y_controller.calculate(
            current_pose.y, desired_state.pose.y
        )
        rot = self.theta_controller.calculate(
            current_pose.rotation().radians(), self.desired_rotation.radians()
        )

        target_chassis_velocities = ChassisVelocities(
            x_speed, y_speed, rot
        ).to_robot_relative(current_pose.rotation())
        self.output_module_states(
            self.kinematics.to_swerve_module_velocities(target_chassis_velocities)
        )

    def end(self, interrupted: bool) -> None:
        self.timer.stop()

    def is_finished(self) -> bool:
        return self.timer.has_elapsed(self.trajectory.duration())
