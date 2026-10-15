#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import rev
import wpilib
from wpimath import Rotation2d, SwerveModulePosition, SwerveModuleVelocity

import configs
from constants import ModuleConstants


class MAXSwerveModule:
    def __init__(
        self, driving_can_id: int, turning_can_id: int, chassis_angular_offset: float
    ) -> None:
        """Constructs a MAXSwerveModule and configures the driving and turning motor,
        encoder, and PID controller. This configuration is specific to the REV
        MAXSwerve Module built with NEOs, SPARKS MAX, and a Through Bore
        Encoder.
        """
        self.driving_spark = rev.SparkMax(
            wpilib.CANPort.CAN_S0, driving_can_id, rev.SparkLowLevel.MotorType.BRUSHLESS
        )
        self.turning_spark = rev.SparkMax(
            wpilib.CANPort.CAN_S0, turning_can_id, rev.SparkLowLevel.MotorType.BRUSHLESS
        )

        self.driving_encoder = self.driving_spark.get_encoder()
        self.turning_encoder = self.turning_spark.get_absolute_encoder()

        self.driving_closed_loop_controller = (
            self.driving_spark.get_closed_loop_controller()
        )
        self.turning_closed_loop_controller = (
            self.turning_spark.get_closed_loop_controller()
        )

        # Apply the respective configurations to the SPARKS. Reset parameters before
        # applying the configuration to bring the SPARK to a known good state. Persist
        # the settings to the SPARK to avoid losing them on a power cycle.
        self.driving_spark.configure(
            configs.MAXSwerveModule.driving_config,
            rev.ResetMode.RESET_SAFE_PARAMETERS,
            rev.PersistMode.PERSIST_PARAMETERS,
        )
        self.turning_spark.configure(
            configs.MAXSwerveModule.turning_config,
            rev.ResetMode.RESET_SAFE_PARAMETERS,
            rev.PersistMode.PERSIST_PARAMETERS,
        )

        self.chassis_angular_offset = chassis_angular_offset
        self.desired_state = SwerveModuleVelocity(
            0.0, Rotation2d(self._get_turning_position())
        )
        self.driving_encoder.set_position(0)

    def _get_driving_position(self) -> float:
        """Returns the distance driven by the wheel, in meters."""
        return (
            self.driving_encoder.get_position().get()
            * ModuleConstants.DRIVING_ENCODER_POSITION_FACTOR
        )

    def _get_driving_velocity(self) -> float:
        """Returns the speed of the wheel, in meters per second."""
        return (
            self.driving_encoder.get_velocity().get()
            * ModuleConstants.DRIVING_ENCODER_VELOCITY_FACTOR
        )

    def _get_turning_position(self) -> float:
        """Returns the angle of the module's absolute encoder, in radians."""
        return (
            self.turning_encoder.get_position().get()
            * ModuleConstants.TURNING_ENCODER_POSITION_FACTOR
        )

    def get_state(self) -> SwerveModuleVelocity:
        """Returns the current state of the module.

        :returns: The current state of the module.
        """
        # Apply chassis angular offset to the encoder position to get the position
        # relative to the chassis.
        return SwerveModuleVelocity(
            self._get_driving_velocity(),
            Rotation2d(self._get_turning_position() - self.chassis_angular_offset),
        )

    def get_position(self) -> SwerveModulePosition:
        """Returns the current position of the module.

        :returns: The current position of the module.
        """
        # Apply chassis angular offset to the encoder position to get the position
        # relative to the chassis.
        return SwerveModulePosition(
            self._get_driving_position(),
            Rotation2d(self._get_turning_position() - self.chassis_angular_offset),
        )

    def set_desired_state(self, desired_state: SwerveModuleVelocity) -> None:
        """Sets the desired state for the module.

        :param desired_state: Desired state with speed and angle.
        """
        # Apply chassis angular offset to the desired state.
        corrected_desired_state = SwerveModuleVelocity(
            desired_state.velocity,
            desired_state.angle + Rotation2d(self.chassis_angular_offset),
        )

        # Optimize the reference state to avoid spinning further than 90 degrees.
        corrected_desired_state = corrected_desired_state.optimize(
            Rotation2d(self._get_turning_position())
        )

        # Command driving and turning SPARKS towards their respective setpoints,
        # converted to the SPARKs' native units (RPM and rotations).
        self.driving_closed_loop_controller.set_setpoint(
            corrected_desired_state.velocity
            / ModuleConstants.DRIVING_ENCODER_VELOCITY_FACTOR,
            rev.SparkBase.ControlType.VELOCITY,
        )
        self.turning_closed_loop_controller.set_setpoint(
            corrected_desired_state.angle.radians()
            / ModuleConstants.TURNING_ENCODER_POSITION_FACTOR,
            rev.SparkBase.ControlType.POSITION,
        )

        self.desired_state = desired_state

    def reset_encoders(self) -> None:
        """Zeroes all the SwerveModule encoders."""
        self.driving_encoder.set_position(0)
