#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import math

import commands2
import hal
import wpilib
from wpimath import (
    ChassisVelocities,
    Pose2d,
    Rotation2d,
    SwerveDrive4Kinematics,
    SwerveDrive4Odometry,
    SwerveModuleVelocity,
)

from constants import DriveConstants
from .maxswervemodule import MAXSwerveModule


class DriveSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        """Creates a new DriveSubsystem."""
        super().__init__()

        # Create MAXSwerveModules
        self.front_left = MAXSwerveModule(
            DriveConstants.FRONT_LEFT_DRIVING_CAN_ID,
            DriveConstants.FRONT_LEFT_TURNING_CAN_ID,
            DriveConstants.FRONT_LEFT_CHASSIS_ANGULAR_OFFSET,
        )

        self.front_right = MAXSwerveModule(
            DriveConstants.FRONT_RIGHT_DRIVING_CAN_ID,
            DriveConstants.FRONT_RIGHT_TURNING_CAN_ID,
            DriveConstants.FRONT_RIGHT_CHASSIS_ANGULAR_OFFSET,
        )

        self.rear_left = MAXSwerveModule(
            DriveConstants.REAR_LEFT_DRIVING_CAN_ID,
            DriveConstants.REAR_LEFT_TURNING_CAN_ID,
            DriveConstants.BACK_LEFT_CHASSIS_ANGULAR_OFFSET,
        )

        self.rear_right = MAXSwerveModule(
            DriveConstants.REAR_RIGHT_DRIVING_CAN_ID,
            DriveConstants.REAR_RIGHT_TURNING_CAN_ID,
            DriveConstants.BACK_RIGHT_CHASSIS_ANGULAR_OFFSET,
        )

        # The gyro sensor
        self.gyro = wpilib.OnboardIMU(wpilib.OnboardIMU.MountOrientation.FLAT)

        # Odometry class for tracking robot pose
        self.odometry = SwerveDrive4Odometry(
            DriveConstants.DRIVE_KINEMATICS,
            Rotation2d(self.gyro.get_yaw()),
            self._get_module_positions(),
        )

        # Usage reporting for MAXSwerve template
        hal.report_usage("RobotDrive", "MAXSwerve")

    def _get_module_positions(self):
        return (
            self.front_left.get_position(),
            self.front_right.get_position(),
            self.rear_left.get_position(),
            self.rear_right.get_position(),
        )

    def periodic(self) -> None:
        # Update the odometry in the periodic block
        self.odometry.update(
            Rotation2d(self.gyro.get_yaw()),
            self._get_module_positions(),
        )

    def get_pose(self) -> Pose2d:
        """Returns the currently-estimated pose of the robot.

        :returns: The pose.
        """
        return self.odometry.get_pose()

    def reset_odometry(self, pose: Pose2d) -> None:
        """Resets the odometry to the specified pose.

        :param pose: The pose to which to set the odometry.
        """
        self.odometry.reset_position(
            Rotation2d(self.gyro.get_yaw()),
            self._get_module_positions(),
            pose,
        )

    def drive(
        self, x_speed: float, y_speed: float, rot: float, field_relative: bool
    ) -> None:
        """Method to drive the robot using joystick info.

        :param x_speed:        Speed of the robot in the x direction (forward).
        :param y_speed:        Speed of the robot in the y direction (sideways).
        :param rot:            Angular rate of the robot.
        :param field_relative: Whether the provided x and y speeds are relative to the
                               field.
        """
        # Convert the commanded speeds into the correct units for the drivetrain
        x_speed_delivered = x_speed * DriveConstants.MAX_SPEED_METERS_PER_SECOND
        y_speed_delivered = y_speed * DriveConstants.MAX_SPEED_METERS_PER_SECOND
        rot_delivered = rot * DriveConstants.MAX_ANGULAR_SPEED

        chassis_velocities = ChassisVelocities(
            x_speed_delivered, y_speed_delivered, rot_delivered
        )
        if field_relative:
            chassis_velocities = chassis_velocities.to_robot_relative(
                Rotation2d(self.gyro.get_yaw())
            )

        swerve_module_states = (
            DriveConstants.DRIVE_KINEMATICS.to_swerve_module_velocities(
                chassis_velocities
            )
        )
        fl, fr, rl, rr = SwerveDrive4Kinematics.desaturate_wheel_velocities(
            swerve_module_states, DriveConstants.MAX_SPEED_METERS_PER_SECOND
        )
        self.front_left.set_desired_state(fl)
        self.front_right.set_desired_state(fr)
        self.rear_left.set_desired_state(rl)
        self.rear_right.set_desired_state(rr)

    def set_x(self) -> None:
        """Sets the wheels into an X formation to prevent movement."""
        self.front_left.set_desired_state(
            SwerveModuleVelocity(0, Rotation2d.from_degrees(45))
        )
        self.front_right.set_desired_state(
            SwerveModuleVelocity(0, Rotation2d.from_degrees(-45))
        )
        self.rear_left.set_desired_state(
            SwerveModuleVelocity(0, Rotation2d.from_degrees(-45))
        )
        self.rear_right.set_desired_state(
            SwerveModuleVelocity(0, Rotation2d.from_degrees(45))
        )

    def set_module_states(
        self,
        desired_states: tuple[
            SwerveModuleVelocity,
            SwerveModuleVelocity,
            SwerveModuleVelocity,
            SwerveModuleVelocity,
        ],
    ) -> None:
        """Sets the swerve ModuleStates.

        :param desired_states: The desired SwerveModule states.
        """
        fl, fr, rl, rr = SwerveDrive4Kinematics.desaturate_wheel_velocities(
            desired_states, DriveConstants.MAX_SPEED_METERS_PER_SECOND
        )
        self.front_left.set_desired_state(fl)
        self.front_right.set_desired_state(fr)
        self.rear_left.set_desired_state(rl)
        self.rear_right.set_desired_state(rr)

    def reset_encoders(self) -> None:
        """Resets the drive encoders to currently read a position of 0."""
        self.front_left.reset_encoders()
        self.rear_left.reset_encoders()
        self.front_right.reset_encoders()
        self.rear_right.reset_encoders()

    def zero_heading(self) -> None:
        """Zeroes the heading of the robot."""
        self.gyro.reset_yaw()

    def get_heading(self) -> float:
        """Returns the heading of the robot.

        :returns: the robot's heading in degrees, from -180 to 180
        """
        return Rotation2d(self.gyro.get_yaw()).degrees()

    def get_turn_rate(self) -> float:
        """Returns the turn rate of the robot.

        :returns: The turn rate of the robot, in degrees per second
        """
        return math.degrees(self.gyro.get_gyro_rate_z()) * (
            -1.0 if DriveConstants.GYRO_REVERSED else 1.0
        )
