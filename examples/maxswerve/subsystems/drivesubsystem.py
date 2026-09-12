#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import math
import typing

import wpilib

from commands2 import Subsystem
from wpimath import (
    ChassisVelocities,
    Pose2d,
    Rotation2d,
    SlewRateLimiter,
    SwerveDrive4Kinematics,
    SwerveDrive4Odometry,
    SwerveModuleVelocity,
)

from constants import DriveConstants
import swerveutils
from .maxswervemodule import MAXSwerveModule


class DriveSubsystem(Subsystem):
    def __init__(self) -> None:
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
        self.gyro = wpilib.OnboardIMU()

        # Slew rate filter variables for controlling lateral acceleration
        self.current_rotation = 0.0
        self.current_translation_dir = 0.0
        self.current_translation_mag = 0.0

        self.mag_limiter = SlewRateLimiter(DriveConstants.MAGNITUDE_SLEW_RATE)
        self.rot_limiter = SlewRateLimiter(DriveConstants.ROTATIONAL_SLEW_RATE)
        self.prev_time = wpilib.Timer.get_timestamp()

        # Odometry class for tracking robot pose
        self.odometry = SwerveDrive4Odometry(
            DriveConstants.DRIVE_KINEMATICS,
            Rotation2d(self.gyro.get_angle_z()),
            (
                self.front_left.get_position(),
                self.front_right.get_position(),
                self.rear_left.get_position(),
                self.rear_right.get_position(),
            ),
        )

    def periodic(self) -> None:
        # Update the odometry in the periodic block
        self.odometry.update(
            Rotation2d(self.gyro.get_angle_z()),
            (
                self.front_left.get_position(),
                self.front_right.get_position(),
                self.rear_left.get_position(),
                self.rear_right.get_position(),
            ),
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
            Rotation2d(self.gyro.get_angle_z()),
            (
                self.front_left.get_position(),
                self.front_right.get_position(),
                self.rear_left.get_position(),
                self.rear_right.get_position(),
            ),
            pose,
        )

    def drive(
        self,
        x_speed: float,
        y_speed: float,
        rot: float,
        field_relative: bool,
        rate_limit: bool,
    ) -> None:
        """Method to drive the robot using joystick info.

        :param x_speed:        Speed of the robot in the x direction (forward).
        :param y_speed:        Speed of the robot in the y direction (sideways).
        :param rot:           Angular rate of the robot.
        :param field_relative: Whether the provided x and y speeds are relative to the
                              field.
        :param rate_limit:     Whether to enable rate limiting for smoother control.
        """

        x_speed_commanded = x_speed
        y_speed_commanded = y_speed

        if rate_limit:
            # Convert XY to polar for rate limiting
            input_translation_dir = math.atan2(y_speed, x_speed)
            input_translation_mag = math.hypot(x_speed, y_speed)

            # Calculate the direction slew rate based on an estimate of the lateral acceleration
            if self.current_translation_mag != 0.0:
                direction_slew_rate = abs(
                    DriveConstants.DIRECTION_SLEW_RATE / self.current_translation_mag
                )
            else:
                direction_slew_rate = 500.0
                # some high number that means the slew rate is effectively instantaneous

            current_time = wpilib.Timer.get_timestamp()
            elapsed_time = current_time - self.prev_time
            angle_difference = swerveutils.angle_difference(
                input_translation_dir, self.current_translation_dir
            )
            if angle_difference < 0.45 * math.pi:
                self.current_translation_dir = swerveutils.step_towards_circular(
                    self.current_translation_dir,
                    input_translation_dir,
                    direction_slew_rate * elapsed_time,
                )
                self.current_translation_mag = self.mag_limiter.calculate(
                    input_translation_mag
                )

            elif angle_difference > 0.85 * math.pi:
                # some small number to avoid floating-point errors with equality checking
                # keep current_translation_dir unchanged
                if self.current_translation_mag > 1e-4:
                    self.current_translation_mag = self.mag_limiter.calculate(0.0)
                else:
                    self.current_translation_dir = swerveutils.wrap_angle(
                        self.current_translation_dir + math.pi
                    )
                    self.current_translation_mag = self.mag_limiter.calculate(
                        input_translation_mag
                    )

            else:
                self.current_translation_dir = swerveutils.step_towards_circular(
                    self.current_translation_dir,
                    input_translation_dir,
                    direction_slew_rate * elapsed_time,
                )
                self.current_translation_mag = self.mag_limiter.calculate(0.0)

            self.prev_time = current_time

            x_speed_commanded = self.current_translation_mag * math.cos(
                self.current_translation_dir
            )
            y_speed_commanded = self.current_translation_mag * math.sin(
                self.current_translation_dir
            )
            self.current_rotation = self.rot_limiter.calculate(rot)

        else:
            self.current_rotation = rot

        # Convert the commanded speeds into the correct units for the drivetrain
        x_speed_delivered = (
            x_speed_commanded * DriveConstants.MAX_SPEED_METERS_PER_SECOND
        )
        y_speed_delivered = (
            y_speed_commanded * DriveConstants.MAX_SPEED_METERS_PER_SECOND
        )
        rot_delivered = self.current_rotation * DriveConstants.MAX_ANGULAR_SPEED

        swerve_module_states = (
            DriveConstants.DRIVE_KINEMATICS.to_swerve_module_velocities(
                ChassisVelocities(
                    x_speed_delivered,
                    y_speed_delivered,
                    rot_delivered,
                ).to_robot_relative(Rotation2d(self.gyro.get_angle_z()))
                if field_relative
                else ChassisVelocities(
                    x_speed_delivered, y_speed_delivered, rot_delivered
                )
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
        desired_states: typing.Tuple[
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
        return Rotation2d(self.gyro.get_angle_z()).degrees()

    def get_turn_rate(self) -> float:
        """Returns the turn rate of the robot.

        :returns: The turn rate of the robot, in radians per second
        """
        return self.gyro.get_gyro_rate_z() * (
            -1.0 if DriveConstants.GYRO_REVERSED else 1.0
        )
