#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

from rev import SparkMax, SparkMaxConfig, ClosedLoopConfig, ResetMode, PersistMode
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState, SwerveModulePosition

from constants import ModuleConstants


class MAXSwerveModule:
    def __init__(
        self, drivingCANId: int, turningCANId: int, chassisAngularOffset: float
    ) -> None:
        """Constructs a MAXSwerveModule and configures the driving and turning motor,
        encoder, and PID controller. This configuration is specific to the REV
        MAXSwerve Module built with NEOs, SPARKS MAX, and a Through Bore
        Encoder.
        """

        self.chassisAngularOffset = 0
        self.desiredState = SwerveModuleState(0.0, Rotation2d())

        self.drivingSparkMax = SparkMax(drivingCANId, SparkMax.MotorType.kBrushless)
        self.turningSparkMax = SparkMax(turningCANId, SparkMax.MotorType.kBrushless)

        self.drivingConfig = SparkMaxConfig()
        self.turningConfig = SparkMaxConfig()

        # Setup encoders and PID controllers for the driving and turning SPARKS MAX.
        self.drivingEncoder = self.drivingSparkMax.getEncoder()
        self.turningEncoder = self.turningSparkMax.getAbsoluteEncoder()
        self.drivingPidController = self.drivingSparkMax.getClosedLoopController()
        self.turningPidController = self.turningSparkMax.getClosedLoopController()
        self.drivingConfig.closedLoop.setFeedbackSensor(
            ClosedLoopConfig.FeedbackSensor.kPrimaryEncoder
        )
        self.turningConfig.closedLoop.setFeedbackSensor(
            ClosedLoopConfig.FeedbackSensor.kAbsoluteEncoder
        )

        # Apply position and velocity conversion factors for the driving encoder. The
        # native units for position and velocity are rotations and RPM, respectively,
        # but we want meters and meters per second to use with WPILib's swerve APIs.
        self.drivingConfig.encoder.positionConversionFactor(
            ModuleConstants.kDrivingEncoderPositionFactor
        )
        self.drivingConfig.encoder.velocityConversionFactor(
            ModuleConstants.kDrivingEncoderVelocityFactor
        )

        # Apply position and velocity conversion factors for the turning encoder. We
        # want these in radians and radians per second to use with WPILib's swerve
        # APIs.
        self.turningConfig.absoluteEncoder.positionConversionFactor(
            ModuleConstants.kTurningEncoderPositionFactor
        )
        self.turningConfig.absoluteEncoder.velocityConversionFactor(
            ModuleConstants.kTurningEncoderVelocityFactor
        )

        # Invert the turning encoder, since the output shaft rotates in the opposite direction of
        # the steering motor in the MAXSwerve Module.
        self.turningConfig.absoluteEncoder.inverted(
            ModuleConstants.kTurningEncoderInverted
        )

        # Enable PID wrap around for the turning motor. This will allow the PID
        # controller to go through 0 to get to the setpoint i.e. going from 350 degrees
        # to 10 degrees will go through 0 rather than the other direction which is a
        # longer route.
        self.turningConfig.closedLoop.positionWrappingEnabled(True)
        self.turningConfig.closedLoop.positionWrappingMinInput(
            ModuleConstants.kTurningEncoderPositionPIDMinInput
        )
        self.turningConfig.closedLoop.positionWrappingMaxInput(
            ModuleConstants.kTurningEncoderPositionPIDMaxInput
        )

        # Set the PID gains for the driving motor. Note these are example gains, and you
        # may need to tune them for your own robot!
        self.drivingConfig.closedLoop.P(ModuleConstants.kDrivingP)
        self.drivingConfig.closedLoop.I(ModuleConstants.kDrivingI)
        self.drivingConfig.closedLoop.D(ModuleConstants.kDrivingD)
        self.drivingConfig.closedLoop.velocityFF(ModuleConstants.kDrivingFF)
        self.drivingConfig.closedLoop.outputRange(
            ModuleConstants.kDrivingMinOutput, ModuleConstants.kDrivingMaxOutput
        )

        # Set the PID gains for the turning motor. Note these are example gains, and you
        # may need to tune them for your own robot!
        self.turningConfig.closedLoop.P(ModuleConstants.kTurningP)
        self.turningConfig.closedLoop.I(ModuleConstants.kTurningI)
        self.turningConfig.closedLoop.D(ModuleConstants.kTurningD)
        self.turningConfig.closedLoop.velocityFF(ModuleConstants.kTurningFF)
        self.turningConfig.closedLoop.outputRange(
            ModuleConstants.kTurningMinOutput, ModuleConstants.kTurningMaxOutput
        )

        self.drivingConfig.setIdleMode(ModuleConstants.kDrivingMotorIdleMode)
        self.turningConfig.setIdleMode(ModuleConstants.kTurningMotorIdleMode)
        # XXX -- can we set current limits?

        # Save the SPARK MAX configurations. If a SPARK MAX browns out during
        # operation, it will maintain the above configurations.
        self.drivingSparkMax.configure(
            self.drivingConfig,
            ResetMode.kResetSafeParameters,
            PersistMode.kPersistParameters,
        )
        self.turningSparkMax.configure(
            self.turningConfig,
            ResetMode.kResetSafeParameters,
            PersistMode.kPersistParameters,
        )

        self.chassisAngularOffset = chassisAngularOffset
        self.desiredState.angle = Rotation2d(self.turningEncoder.getPosition())
        self.drivingEncoder.setPosition(0)

    def getState(self) -> SwerveModuleState:
        """Returns the current state of the module.

        :returns: The current state of the module.
        """
        # Apply chassis angular offset to the encoder position to get the position
        # relative to the chassis.
        return SwerveModuleState(
            self.drivingEncoder.getVelocity(),
            Rotation2d(self.turningEncoder.getPosition() - self.chassisAngularOffset),
        )

    def getPosition(self) -> SwerveModulePosition:
        """Returns the current position of the module.

        :returns: The current position of the module.
        """
        # Apply chassis angular offset to the encoder position to get the position
        # relative to the chassis.
        return SwerveModulePosition(
            self.drivingEncoder.getPosition(),
            Rotation2d(self.turningEncoder.getPosition() - self.chassisAngularOffset),
        )

    def setDesiredState(self, desiredState: SwerveModuleState) -> None:
        """Sets the desired state for the module.

        :param desiredState: Desired state with speed and angle.

        """
        # Apply chassis angular offset to the desired state.
        correctedDesiredState = SwerveModuleState()
        correctedDesiredState.speed = desiredState.speed
        correctedDesiredState.angle = desiredState.angle + Rotation2d(
            self.chassisAngularOffset
        )

        # Optimize the reference state to avoid spinning further than 90 degrees.
        SwerveModuleState.optimize(
            correctedDesiredState, Rotation2d(self.turningEncoder.getPosition())
        )

        # Command driving and turning SPARKS MAX towards their respective setpoints.
        self.drivingPidController.setReference(
            correctedDesiredState.speed, SparkMax.ControlType.kVelocity
        )
        self.turningPidController.setReference(
            correctedDesiredState.angle.radians(), SparkMax.ControlType.kPosition
        )

        self.desiredState = desiredState

    def resetEncoders(self) -> None:
        """
        Zeroes all the SwerveModule encoders.
        """
        self.drivingEncoder.setPosition(0)
