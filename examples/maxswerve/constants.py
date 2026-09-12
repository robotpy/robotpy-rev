#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

"""
The constants module is a convenience place for teams to hold robot-wide
numerical or boolean constants. Don't use this for any other purpose!
"""

import math

from wpimath import SwerveDrive4Kinematics, Translation2d, units

from rev import SparkBaseConfig


class NeoMotorConstants:
    FREE_SPEED_RPM = 5676


class DriveConstants:
    # Driving Parameters - Note that these are not the maximum capable speeds of
    # the robot, rather the allowed maximum speeds
    MAX_SPEED_METERS_PER_SECOND = 4.8
    MAX_ANGULAR_SPEED = math.tau  # radians per second

    DIRECTION_SLEW_RATE = 1.2  # radians per second
    MAGNITUDE_SLEW_RATE = 1.8  # percent per second (1 = 100%)
    ROTATIONAL_SLEW_RATE = 2.0  # percent per second (1 = 100%)

    # Chassis configuration
    TRACK_WIDTH = units.inches_to_meters(26.5)
    # Distance between centers of right and left wheels on robot
    WHEEL_BASE = units.inches_to_meters(26.5)

    # Distance between front and back wheels on robot
    MODULE_POSITIONS = [
        Translation2d(WHEEL_BASE / 2, TRACK_WIDTH / 2),
        Translation2d(WHEEL_BASE / 2, -TRACK_WIDTH / 2),
        Translation2d(-WHEEL_BASE / 2, TRACK_WIDTH / 2),
        Translation2d(-WHEEL_BASE / 2, -TRACK_WIDTH / 2),
    ]
    DRIVE_KINEMATICS = SwerveDrive4Kinematics(*MODULE_POSITIONS)

    # Angular offsets of the modules relative to the chassis in radians
    FRONT_LEFT_CHASSIS_ANGULAR_OFFSET = -math.pi / 2
    FRONT_RIGHT_CHASSIS_ANGULAR_OFFSET = 0
    BACK_LEFT_CHASSIS_ANGULAR_OFFSET = math.pi
    BACK_RIGHT_CHASSIS_ANGULAR_OFFSET = math.pi / 2

    # SPARK MAX CAN IDs
    FRONT_LEFT_DRIVING_CAN_ID = 11
    REAR_LEFT_DRIVING_CAN_ID = 13
    FRONT_RIGHT_DRIVING_CAN_ID = 15
    REAR_RIGHT_DRIVING_CAN_ID = 17

    FRONT_LEFT_TURNING_CAN_ID = 10
    REAR_LEFT_TURNING_CAN_ID = 12
    FRONT_RIGHT_TURNING_CAN_ID = 14
    REAR_RIGHT_TURNING_CAN_ID = 16

    GYRO_REVERSED = False


class ModuleConstants:
    # The MAXSwerve module can be configured with one of three pinion gears: 12T, 13T, or 14T.
    # This changes the drive speed of the module (a pinion gear with more teeth will result in a
    # robot that drives faster).
    DRIVING_MOTOR_PINION_TEETH = 14

    # Invert the turning encoder, since the output shaft rotates in the opposite direction of
    # the steering motor in the MAXSwerve Module.
    TURNING_ENCODER_INVERTED = True

    # Calculations required for driving motor conversion factors and feed forward
    DRIVING_MOTOR_FREE_SPEED_RPS = NeoMotorConstants.FREE_SPEED_RPM / 60
    WHEEL_DIAMETER_METERS = 0.0762
    WHEEL_CIRCUMFERENCE_METERS = WHEEL_DIAMETER_METERS * math.pi
    # 45 teeth on the wheel's bevel gear, 22 teeth on the first-stage spur gear, 15 teeth on the bevel pinion
    DRIVING_MOTOR_REDUCTION = (45.0 * 22) / (DRIVING_MOTOR_PINION_TEETH * 15)
    DRIVE_WHEEL_FREE_SPEED_RPS = (
        DRIVING_MOTOR_FREE_SPEED_RPS * WHEEL_CIRCUMFERENCE_METERS
    ) / DRIVING_MOTOR_REDUCTION

    DRIVING_ENCODER_POSITION_FACTOR = (
        WHEEL_DIAMETER_METERS * math.pi
    ) / DRIVING_MOTOR_REDUCTION  # meters
    DRIVING_ENCODER_VELOCITY_FACTOR = (
        (WHEEL_DIAMETER_METERS * math.pi) / DRIVING_MOTOR_REDUCTION
    ) / 60.0  # meters per second

    TURNING_ENCODER_POSITION_FACTOR = math.tau  # radian
    TURNING_ENCODER_VELOCITY_FACTOR = math.tau / 60.0  # radians per second

    TURNING_ENCODER_POSITION_PID_MIN_INPUT = 0  # radian
    TURNING_ENCODER_POSITION_PID_MAX_INPUT = TURNING_ENCODER_POSITION_FACTOR  # radian

    DRIVING_P = 0.04
    DRIVING_I = 0
    DRIVING_D = 0
    DRIVING_FF = 1 / DRIVE_WHEEL_FREE_SPEED_RPS
    DRIVING_MIN_OUTPUT = -1
    DRIVING_MAX_OUTPUT = 1

    TURNING_P = 1
    TURNING_I = 0
    TURNING_D = 0
    TURNING_FF = 0
    TURNING_MIN_OUTPUT = -1
    TURNING_MAX_OUTPUT = 1

    DRIVING_MOTOR_IDLE_MODE = SparkBaseConfig.IdleMode.BRAKE
    TURNING_MOTOR_IDLE_MODE = SparkBaseConfig.IdleMode.BRAKE

    DRIVING_MOTOR_CURRENT_LIMIT = 50  # amp
    TURNING_MOTOR_CURRENT_LIMIT = 20  # amp


class OIConstants:
    DRIVER_CONTROLLER_PORT = 0
    DRIVE_DEADBAND = 0.05


class AutoConstants:
    MAX_SPEED_METERS_PER_SECOND = 3
    MAX_ACCELERATION_METERS_PER_SECOND_SQUARED = 3
    MAX_ANGULAR_SPEED_RADIANS_PER_SECOND = math.pi
    MAX_ANGULAR_SPEED_RADIANS_PER_SECOND_SQUARED = math.pi
