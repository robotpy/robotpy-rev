#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

from rev import (
    SparkBase,
    SparkLowLevel,
    SparkMax,
    SparkMaxConfig,
    ClosedLoopConfig,
    ResetMode,
    PersistMode,
)
from wpimath import Rotation2d, SwerveModulePosition, SwerveModuleVelocity

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

        self.chassis_angular_offset = 0
        self.desired_state = SwerveModuleVelocity(0.0, Rotation2d())

        self.driving_spark_max = SparkMax(
            0, driving_can_id, SparkLowLevel.MotorType.BRUSHLESS
        )
        self.turning_spark_max = SparkMax(
            0, turning_can_id, SparkLowLevel.MotorType.BRUSHLESS
        )

        self.driving_config = SparkMaxConfig()
        self.turning_config = SparkMaxConfig()

        # Setup encoders and PID controllers for the driving and turning SPARKS MAX.
        self.driving_encoder = self.driving_spark_max.get_encoder()
        self.turning_encoder = self.turning_spark_max.get_absolute_encoder()
        self.driving_pid_controller = (
            self.driving_spark_max.get_closed_loop_controller()
        )
        self.turning_pid_controller = (
            self.turning_spark_max.get_closed_loop_controller()
        )
        self.driving_config.closed_loop.set_feedback_sensor(
            ClosedLoopConfig.FeedbackSensor.PRIMARY_ENCODER
        )
        self.turning_config.closed_loop.set_feedback_sensor(
            ClosedLoopConfig.FeedbackSensor.ABSOLUTE_ENCODER
        )

        # Apply position and velocity conversion factors for the driving encoder. The
        # native units for position and velocity are rotations and RPM, respectively,
        # but we want meters and meters per second to use with WPILib's swerve APIs.
        self.driving_config.encoder.position_conversion_factor(
            ModuleConstants.DRIVING_ENCODER_POSITION_FACTOR
        )
        self.driving_config.encoder.velocity_conversion_factor(
            ModuleConstants.DRIVING_ENCODER_VELOCITY_FACTOR
        )

        # Apply position and velocity conversion factors for the turning encoder. We
        # want these in radians and radians per second to use with WPILib's swerve
        # APIs.
        self.turning_config.absolute_encoder.position_conversion_factor(
            ModuleConstants.TURNING_ENCODER_POSITION_FACTOR
        )
        self.turning_config.absolute_encoder.velocity_conversion_factor(
            ModuleConstants.TURNING_ENCODER_VELOCITY_FACTOR
        )

        # Invert the turning encoder, since the output shaft rotates in the opposite direction of
        # the steering motor in the MAXSwerve Module.
        self.turning_config.absolute_encoder.inverted(
            ModuleConstants.TURNING_ENCODER_INVERTED
        )

        # Enable PID wrap around for the turning motor. This will allow the PID
        # controller to go through 0 to get to the setpoint i.e. going from 350 degrees
        # to 10 degrees will go through 0 rather than the other direction which is a
        # longer route.
        self.turning_config.closed_loop.position_wrapping_enabled(True)
        self.turning_config.closed_loop.position_wrapping_min_input(
            ModuleConstants.TURNING_ENCODER_POSITION_PID_MIN_INPUT
        )
        self.turning_config.closed_loop.position_wrapping_max_input(
            ModuleConstants.TURNING_ENCODER_POSITION_PID_MAX_INPUT
        )

        # Set the PID gains for the driving motor. Note these are example gains, and you
        # may need to tune them for your own robot!
        self.driving_config.closed_loop.P(ModuleConstants.DRIVING_P)
        self.driving_config.closed_loop.I(ModuleConstants.DRIVING_I)
        self.driving_config.closed_loop.D(ModuleConstants.DRIVING_D)
        self.driving_config.closed_loop.velocity_ff(ModuleConstants.DRIVING_FF)
        self.driving_config.closed_loop.output_range(
            ModuleConstants.DRIVING_MIN_OUTPUT, ModuleConstants.DRIVING_MAX_OUTPUT
        )

        # Set the PID gains for the turning motor. Note these are example gains, and you
        # may need to tune them for your own robot!
        self.turning_config.closed_loop.P(ModuleConstants.TURNING_P)
        self.turning_config.closed_loop.I(ModuleConstants.TURNING_I)
        self.turning_config.closed_loop.D(ModuleConstants.TURNING_D)
        self.turning_config.closed_loop.velocity_ff(ModuleConstants.TURNING_FF)
        self.turning_config.closed_loop.output_range(
            ModuleConstants.TURNING_MIN_OUTPUT, ModuleConstants.TURNING_MAX_OUTPUT
        )

        self.driving_config.set_idle_mode(ModuleConstants.DRIVING_MOTOR_IDLE_MODE)
        self.turning_config.set_idle_mode(ModuleConstants.TURNING_MOTOR_IDLE_MODE)
        # XXX -- can we set current limits?

        # Save the SPARK MAX configurations. If a SPARK MAX browns out during
        # operation, it will maintain the above configurations.
        self.driving_spark_max.configure(
            self.driving_config,
            ResetMode.RESET_SAFE_PARAMETERS,
            PersistMode.PERSIST_PARAMETERS,
        )
        self.turning_spark_max.configure(
            self.turning_config,
            ResetMode.RESET_SAFE_PARAMETERS,
            PersistMode.PERSIST_PARAMETERS,
        )

        self.chassis_angular_offset = chassis_angular_offset
        self.desired_state.angle = Rotation2d(self.turning_encoder.get_position())
        self.driving_encoder.set_position(0)

    def get_state(self) -> SwerveModuleVelocity:
        """Returns the current state of the module.

        :returns: The current state of the module.
        """
        # Apply chassis angular offset to the encoder position to get the position
        # relative to the chassis.
        return SwerveModuleVelocity(
            self.driving_encoder.get_velocity(),
            Rotation2d(
                self.turning_encoder.get_position() - self.chassis_angular_offset
            ),
        )

    def get_position(self) -> SwerveModulePosition:
        """Returns the current position of the module.

        :returns: The current position of the module.
        """
        # Apply chassis angular offset to the encoder position to get the position
        # relative to the chassis.
        return SwerveModulePosition(
            self.driving_encoder.get_position(),
            Rotation2d(
                self.turning_encoder.get_position() - self.chassis_angular_offset
            ),
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
            Rotation2d(self.turning_encoder.get_position())
        )

        # Command driving and turning SPARKS MAX towards their respective setpoints.
        self.driving_pid_controller.set_reference(
            corrected_desired_state.velocity, SparkBase.ControlType.VELOCITY
        )
        self.turning_pid_controller.set_reference(
            corrected_desired_state.angle.radians(), SparkBase.ControlType.POSITION
        )

        self.desired_state = desired_state

    def reset_encoders(self) -> None:
        """
        Zeroes all the SwerveModule encoders.
        """
        self.driving_encoder.set_position(0)
