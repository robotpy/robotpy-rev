from rev import CANSparkMax, SparkMaxAbsoluteEncoder
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

        self.drivingSparkMax = CANSparkMax(
            drivingCANId, CANSparkMax.MotorType.kBrushless
        )
        self.turningSparkMax = CANSparkMax(
            turningCANId, CANSparkMax.MotorType.kBrushless
        )

        # Factory reset, so we get the SPARKS MAX to a known state before configuring
        # them. This is useful in case a SPARK MAX is swapped out.
        self.drivingSparkMax.restoreFactoryDefaults()
        self.turningSparkMax.restoreFactoryDefaults()

        # Setup encoders and PID controllers for the driving and turning SPARKS MAX.
        self.drivingEncoder = self.drivingSparkMax.getEncoder()
        self.turningEncoder = self.turningSparkMax.getAbsoluteEncoder(
            SparkMaxAbsoluteEncoder.Type.kDutyCycle
        )
        self.drivingPIDController = self.drivingSparkMax.getPIDController()
        self.turningPIDController = self.turningSparkMax.getPIDController()
        self.drivingPIDController.setFeedbackDevice(self.drivingEncoder)
        self.turningPIDController.setFeedbackDevice(self.turningEncoder)

        # Apply position and velocity conversion factors for the driving encoder. The
        # native units for position and velocity are rotations and RPM, respectively,
        # but we want meters and meters per second to use with WPILib's swerve APIs.
        self.drivingEncoder.setPositionConversionFactor(
            ModuleConstants.kDrivingEncoderPositionFactor
        )
        self.drivingEncoder.setVelocityConversionFactor(
            ModuleConstants.kDrivingEncoderVelocityFactor
        )

        # Apply position and velocity conversion factors for the turning encoder. We
        # want these in radians and radians per second to use with WPILib's swerve
        # APIs.
        self.turningEncoder.setPositionConversionFactor(
            ModuleConstants.kTurningEncoderPositionFactor
        )
        self.turningEncoder.setVelocityConversionFactor(
            ModuleConstants.kTurningEncoderVelocityFactor
        )

        # Invert the turning encoder, since the output shaft rotates in the opposite direction of
        # the steering motor in the MAXSwerve Module.
        self.turningEncoder.setInverted(ModuleConstants.kTurningEncoderInverted)

        # Enable PID wrap around for the turning motor. This will allow the PID
        # controller to go through 0 to get to the setpoint i.e. going from 350 degrees
        # to 10 degrees will go through 0 rather than the other direction which is a
        # longer route.
        self.turningPIDController.setPositionPIDWrappingEnabled(True)
        self.turningPIDController.setPositionPIDWrappingMinInput(
            ModuleConstants.kTurningEncoderPositionPIDMinInput
        )
        self.turningPIDController.setPositionPIDWrappingMaxInput(
            ModuleConstants.kTurningEncoderPositionPIDMaxInput
        )

        # Set the PID gains for the driving motor. Note these are example gains, and you
        # may need to tune them for your own robot!
        self.drivingPIDController.setP(ModuleConstants.kDrivingP)
        self.drivingPIDController.setI(ModuleConstants.kDrivingI)
        self.drivingPIDController.setD(ModuleConstants.kDrivingD)
        self.drivingPIDController.setFF(ModuleConstants.kDrivingFF)
        self.drivingPIDController.setOutputRange(
            ModuleConstants.kDrivingMinOutput, ModuleConstants.kDrivingMaxOutput
        )

        # Set the PID gains for the turning motor. Note these are example gains, and you
        # may need to tune them for your own robot!
        self.turningPIDController.setP(ModuleConstants.kTurningP)
        self.turningPIDController.setI(ModuleConstants.kTurningI)
        self.turningPIDController.setD(ModuleConstants.kTurningD)
        self.turningPIDController.setFF(ModuleConstants.kTurningFF)
        self.turningPIDController.setOutputRange(
            ModuleConstants.kTurningMinOutput, ModuleConstants.kTurningMaxOutput
        )

        self.drivingSparkMax.setIdleMode(ModuleConstants.kDrivingMotorIdleMode)
        self.turningSparkMax.setIdleMode(ModuleConstants.kTurningMotorIdleMode)
        self.drivingSparkMax.setSmartCurrentLimit(
            ModuleConstants.kDrivingMotorCurrentLimit
        )
        self.turningSparkMax.setSmartCurrentLimit(
            ModuleConstants.kTurningMotorCurrentLimit
        )

        # Save the SPARK MAX configurations. If a SPARK MAX browns out during
        # operation, it will maintain the above configurations.
        self.drivingSparkMax.burnFlash()
        self.turningSparkMax.burnFlash()

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
        optimizedDesiredState = SwerveModuleState.optimize(
            correctedDesiredState, Rotation2d(self.turningEncoder.getPosition())
        )

        # Command driving and turning SPARKS MAX towards their respective setpoints.
        self.drivingPIDController.setReference(
            optimizedDesiredState.speed, CANSparkMax.ControlType.kVelocity
        )
        self.turningPIDController.setReference(
            optimizedDesiredState.angle.radians(), CANSparkMax.ControlType.kPosition
        )

        self.desiredState = desiredState

    def resetEncoders(self) -> None:
        """
        Zeroes all the SwerveModule encoders.
        """
        self.drivingEncoder.setPosition(0)
