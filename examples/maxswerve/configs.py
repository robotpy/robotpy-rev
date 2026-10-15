#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import rev

from constants import ModuleConstants


class MAXSwerveModule:
    driving_config = rev.SparkMaxConfig()
    turning_config = rev.SparkMaxConfig()

    # Use module constants to calculate the feed forward gain.
    nominal_voltage = 12.0
    driving_velocity_feed_forward = (
        nominal_voltage / ModuleConstants.DRIVE_WHEEL_FREE_SPEED_RPS
    )  # volts per meter per second

    # REVLib 2027 removed the encoder conversion factors, so the closed loops run
    # in native units: RPM for the driving encoder and rotations for the absolute
    # encoder. The gains below are written in meters per second and radians (the
    # units REV's template configures) and scaled to native units.
    driving_factor = ModuleConstants.DRIVING_ENCODER_VELOCITY_FACTOR  # m/s per RPM
    turning_factor = ModuleConstants.TURNING_ENCODER_POSITION_FACTOR  # rad per rot

    driving_config.set_idle_mode(rev.SparkBaseConfig.IdleMode.BRAKE)
    driving_config.smart_current_limit(50)
    driving_config.closed_loop.set_feedback_sensor(rev.FeedbackSensor.PRIMARY_ENCODER)
    # These are example gains you may need to tune for your own robot!
    driving_config.closed_loop.pid(0.04 * driving_factor, 0, 0)
    driving_config.closed_loop.output_range(-1, 1)
    driving_config.closed_loop.feed_forward.v(
        driving_velocity_feed_forward * driving_factor
    )

    turning_config.set_idle_mode(rev.SparkBaseConfig.IdleMode.BRAKE)
    turning_config.smart_current_limit(20)

    # Invert the turning encoder, since the output shaft rotates in the opposite
    # direction of the steering motor in the MAXSwerve Module.
    turning_config.absolute_encoder.inverted(True)
    # This applies to REV Through Bore Encoder V2 (use rev_through_bore_encoder for V1):
    turning_config.absolute_encoder.apply(
        rev.AbsoluteEncoderConfig.Presets.rev_through_bore_encoder_v2()
    )

    turning_config.closed_loop.set_feedback_sensor(rev.FeedbackSensor.ABSOLUTE_ENCODER)
    # These are example gains you may need to tune for your own robot!
    turning_config.closed_loop.pid(1 * turning_factor, 0, 0)
    turning_config.closed_loop.output_range(-1, 1)
    # Enable PID wrap around for the turning motor. This will allow the PID
    # controller to go through 0 to get to the setpoint i.e. going from 350 degrees
    # to 10 degrees will go through 0 rather than the other direction which is a
    # longer route. The controller wraps over the encoder's range of one rotation.
    turning_config.closed_loop.position_wrapping_enabled(True)
